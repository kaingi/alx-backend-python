# chats/middleware.py
from django.http import JsonResponse
import logging
from datetime import datetime
from django.http import HttpResponseForbidden

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)

        # Only restrict if the user is authenticated
        if user and user.is_authenticated:
            # Check if user is NOT admin or moderator
            if not (user.is_superuser or getattr(user, "role", None) in ["admin", "moderator"]):
                return JsonResponse({"error": "Forbidden: Insufficient permissions"}, status=403)

        return self.get_response(request)
    
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.offensive_words = ['badword1', 'badword2', 'badword3']  # Replace with actual offensive words

    def __call__(self, request):
        if request.method == 'POST':
            message = request.POST.get('message', '').lower()
            if any(word in message for word in self.offensive_words):
                return HttpResponseForbidden("Your message contains inappropriate language.")

        return self.get_response(request)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(message)s'
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_entry)
        response = self.get_response(request)
        return response
