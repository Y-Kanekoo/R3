# middleware.py
from django.shortcuts import redirect
from django.conf import settings

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.session.get_expiry_age():
            return redirect(settings.LOGIN_URL)
        response = self.get_response(request)
        return response
