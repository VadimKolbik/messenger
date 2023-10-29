from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chats.urls', namespace='chats')),
    path('users/', include('users.urls', namespace='users')),
]
