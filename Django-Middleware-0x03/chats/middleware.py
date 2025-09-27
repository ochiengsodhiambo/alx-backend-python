import logging
import time
from datetime import datetime
from collections import defaultdict

from django.http import JsonResponse, HttpResponseForbidden

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    """
    Logs every request with user and path.
    Format: "2025-09-27 12:00:00 - User: <user> - Path: /api/messages/"
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    """
    Denies access outside business hours (6AM - 9PM).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden("Access to the chat is restricted at this time.")
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    """
    Limits users to 5 POST requests per minute per IP.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # {ip: [timestamps]}
        self.requests_log = defaultdict(list)

    def __call__(self, request):
        if request.method == "POST" and "/messages" in request.path:
            ip = request.META.get("REMOTE_ADDR", "unknown")
            now = time.time()

            # keep only timestamps within last 60s
            self.requests_log[ip] = [t for t in self.requests_log[ip] if now - t < 60]

            if len(self.requests_log[ip]) >= 5:
                return JsonResponse(
                    {"error": "Rate limit exceeded. Max 5 messages per minute."},
                    status=429
                )

            self.requests_log[ip].append(now)

            # cleanup old IPs with no timestamps
            if not self.requests_log[ip]:
                del self.requests_log[ip]

        return self.get_response(request)


class RolePermissionMiddleware:
    """
    Allows only admin or moderator users for certain restricted paths.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        restricted_paths = ["/admin/", "/messages/delete/"]

        if any(request.path.startswith(p) for p in restricted_paths):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required.")

            # Check roles (adjust if your User model has custom roles)
            if not (request.user.is_staff or getattr(request.user, "role", None) in ["admin", "moderator"]):
                return HttpResponseForbidden("You do not have permission to access this resource.")

        return self.get_response(request)
