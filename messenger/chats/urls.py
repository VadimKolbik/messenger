from django.urls import path
from .views import *

app_name = 'chats'

urlpatterns = [
    path('', index, name='index'),
    path('chats/', ChatsView.as_view(), name='all_chats'),
    path('chats/<int:chat_id>/', ChatView.as_view(), name='chat'),
]