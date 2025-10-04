import logging
import time
from datetime import datetime
from collections import defaultdict
from django.http import HttpResponseForbidden, JsonResponse

logger = logging.getLogger("chats")


# 1. Request Logging
class RequestLoggingMiddleware:
    """
    Logs every request with user and path.
    Format: "2025-09-27 12:00:00 - User: <user> - Path: /api/messages/"
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # âœ… Always allow admin paths
        if request.path.startswith("/admin/"):
            return self.get_response(request)

        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)
        return self.get_response(request)


# 2. Restrict Access by Time
class RestrictAccessByTimeMiddleware:
    """
    Denies access outside business hours (6AM - 9PM).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # âœ… Always allow admin paths
        if request.path.startswith("/admin/"):
            return self.get_response(request)

        current_hour = datetime.now().hour
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden("Access to the chat is restricted at this time.")
        return self.get_response(request)


# 3. Rate Limiting / Offensive Language
class OffensiveLanguageMiddleware:
    """
    Limits users to 5 POST requests per minute per IP.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_log = defaultdict(list)  # {ip: [timestamps]}

    def __call__(self, request):
        # âœ… Always allow admin paths
        if request.path.startswith("/admin/"):
            return self.get_response(request)

        if request.method == "POST" and "/messages" in request.path:
            ip = request.META.get("REMOTE_ADDR", "unknown")
            now = time.time()

            # Keep only timestamps within the last 60 seconds
            self.requests_log[ip] = [t for t in self.requests_log[ip] if now - t < 60]

            if len(self.requests_log[ip]) >= 5:
                return JsonResponse(
                    {"error": "Rate limit exceeded. Max 5 messages per minute."},
                    status=429
                )

            self.requests_log[ip].append(now)

        return self.get_response(request)


# 4. Role-based Permissions
class RolePermissionMiddleware:
    """
    Allows only admin or moderator users for restricted paths.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # âœ… Always allow admin paths
        if request.path.startswith("/admin/"):
            return self.get_response(request)

        restricted_paths = ["/messages/delete/"]  # admin already allowed above

        if any(request.path.startswith(p) for p in restricted_paths):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required.")

            if not (request.user.is_staff or getattr(request.user, "role", None) in ["admin", "moderator"]):
                return HttpResponseForbidden("You do not have permission to access this resource.")

        return self.get_response(request)

