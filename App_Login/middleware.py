"""
Custom security middleware for additional protection
"""
from django.http import HttpResponseForbidden
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


class SecurityMiddleware:
    """
    Additional security middleware for the application
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Add security headers
        response = self.get_response(request)
        
        # Add custom security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'same-origin'
        
        # Add basic Content Security Policy
        if not hasattr(response, 'get') or response.get('Content-Type', '').startswith('text/html'):
            response['Content-Security-Policy'] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self' data:;"
            )
        
        return response


class SuspiciousActivityMiddleware:
    """
    Monitor and block suspicious activity
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.suspicious_patterns = [
            '../',  # Directory traversal
            '<script',  # XSS attempts
            'union select',  # SQL injection
            'drop table',  # SQL injection
        ]

    def __call__(self, request):
        # Check for suspicious patterns in request
        request_data = str(request.GET) + str(request.POST)
        
        for pattern in self.suspicious_patterns:
            if pattern.lower() in request_data.lower():
                ip = request.META.get('REMOTE_ADDR')
                logger.warning(f'Suspicious activity detected from {ip}: {pattern}')
                
                # Increment suspicious activity counter
                cache_key = f'suspicious_{ip}'
                count = cache.get(cache_key, 0)
                cache.set(cache_key, count + 1, 86400)  # 24 hours
                
                # Block if too many suspicious requests
                if count > 10:
                    logger.error(f'Blocking IP {ip} due to repeated suspicious activity')
                    return HttpResponseForbidden('Access Denied')
        
        response = self.get_response(request)
        return response
