# chats/middleware.py

import logging
from datetime import datetime
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define allowed time range: 6 PM to 9 PM
        start_time = time(18, 0)  # 6:00 PM
        end_time = time(21, 0)    # 9:00 PM

        current_time = datetime.now().time()

        # Apply restriction only on /chats/ or similar chat endpoints
        if request.path.startswith('/chats/'):
            if current_time < start_time or current_time > end_time:
                return HttpResponseForbidden("Access to chat is restricted outside 6PM to 9PM.")

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
