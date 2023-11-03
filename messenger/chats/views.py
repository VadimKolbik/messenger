from django.db import models
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q
from django.urls import reverse

from .models import *
from users.models import CustomUser
from .forms import MessageForm

from django.contrib.auth.mixins import LoginRequiredMixin

class MyLoginRequiredView(LoginRequiredMixin):
    login_url = '/users/login'

menu = [
    {'title': 'Главная', 'url': 'home'},
    {'title': 'Регистрация', 'url': 'users:login'},
    {'title': 'Авторизация', 'url': 'users:login'},
]

class ChatView(MyLoginRequiredView, DetailView):
    '''Chat between 2 users'''
    model = Chat
    template_name = 'chats/chat.html'
    context_object_name = 'messages'
    pk_url_kwarg = 'chat_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Чат'
        context['form'] = MessageForm()
        return context
    
    def post(self, request, chat_id):
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.sender = request.user
            message.save()
        return redirect(reverse('chats:chat', kwargs={'chat_id': chat_id}))


class ChatsView(MyLoginRequiredView, ListView):
    '''All chats of users'''
    model = Chat
    template_name = 'chats/chats.html'
    context_object_name = 'chats'

    def get_queryset(self):
        return Chat.objects.filter(members__in=[self.request.user.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def index(request):
    return render(request, 'chats/index.html')