from django.urls import path
from .views import *

app_name = 'chats'

urlpatterns = [
    path('', index, name='index'),
    path('chats/', ChatsView.as_view(), name='all_chats'),
    path('chats/<int:chat_id>/', ChatView.as_view(), name='chat'),
    path('chats/create/<int:user_id>/', CreateChatView.as_view(), name='create_chat'),
    path('group_chat/create/<int:user_id>/', CreateGroupChatView.as_view(), name='create_group_chat'),
    path('chats/info/<int:chat_id>/', InfoAboutChatView.as_view(), name='info_about_chat'),
    path('chats/info/<int:chat_id>/delete_user/<int:user_id>/', delete_user_from_group_chat, name='delete_user_from_chat'),
    path('chats/info/<int:chat_id>/add_user/<int:user_id>/', add_user_in_group_chat, name='add_user_in_chat'),
    path('chats/info/<int:chat_id>/delete/', chat_delete_view, name='delete_group_chat'),
    path('chats/info/<int:chat_id>/rename_chat/', rename_group_chat, name='rename_group_chat'),
]