from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

class UpdateOnlineStatusMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response
    
    def __call__(self, request):
        user = request.user
        if not isinstance(user, AnonymousUser):
            user.last_online = timezone.now()
            user.save(update_fields=['last_online'])
        response = self.get_response(request)
        return response