from django.urls import path
from .views import *

app_name = 'chats'

urlpatterns = [
    path('', index, name='home'),
    path('<int:sen_pk>-<int:rec_pk>/', Chat.as_view(), name='chat'),
    path('chats/<int:user_pk>/', Chats.as_view(), name='chats'),
]