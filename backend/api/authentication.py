from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication without CSRF enforcement for REST API clients.
    Allows frontend fetch requests to authenticate via cookies/sessions
    without requiring manual CSRF token headers.
    """
    def enforce_csrf(self, request):
        return  # CSRF check exempted for REST API endpoints
