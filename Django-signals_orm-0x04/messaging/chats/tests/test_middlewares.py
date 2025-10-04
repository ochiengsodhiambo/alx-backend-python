from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from chats.middleware import (
    RequestLoggingMiddleware,
    RestrictAccessByTimeMiddleware,
    OffensiveLanguageMiddleware,
    RolePermissionMiddleware,
)

User = get_user_model()

class TestMiddlewares(TestCase):  # 👈 starts with “Test”
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="tester", password="12345")

    def test_request_logging_middleware(self):
        request = self.factory.get("/api/messages/")
        request.user = self.user
        response = RequestLoggingMiddleware(lambda r: HttpResponse("ok"))(request)
        self.assertEqual(response.status_code, 200)

    def test_restrict_access_by_time_middleware_allows_during_day(self):
        request = self.factory.get("/api/messages/")
        middleware = RestrictAccessByTimeMiddleware(lambda r: HttpResponse("ok"))
        response = middleware(request)
        self.assertEqual(response.status_code, 200)

    def test_offensive_language_rate_limit(self):
        request = self.factory.post("/api/messages/")
        middleware = OffensiveLanguageMiddleware(lambda r: HttpResponse("ok"))
        for _ in range(5):
            middleware(request)
        response = middleware(request)
        self.assertEqual(response.status_code, 429)

    def test_role_permission_middleware_admin_access(self):
        request = self.factory.get("/admin/")
        request.user = self.user
        self.user.is_staff = True
        middleware = RolePermissionMiddleware(lambda r: HttpResponse("ok"))
        response = middleware(request)
        self.assertEqual(response.status_code, 200)
