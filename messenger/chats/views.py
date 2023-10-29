from typing import Any
from django.db import models
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from django.db.models import Q

from .models import *
from users.models import CustomUser
menu = [
    {'title': 'Главная', 'url': 'home'},
    {'title': 'Регистрация', 'url': 'users:login'},
    {'title': 'Авторизация', 'url': 'users:login'},
]

class Chat(ListView):
    '''Chat with in only user'''
    model = Messange
    template_name = 'chats/chat.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Messange.objects.filter(Q(resepien=self.kwargs['rec_pk']) | Q(resepien=self.kwargs['sen_pk'])).filter(Q(sender=self.kwargs['rec_pk']) | Q(sender=self.kwargs['sen_pk'])).order_by('time_create')
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Чат'
        print(self.kwargs['sen_pk'])
        return context


class Chats(DetailView):
    '''All chats with all users'''
    model = CustomUser
    template_name = 'chats/chats.html'
    context_object_name = 'customuser'
    pk_url_kwarg = 'user_pk'

    # def get_queryset(self):
    #     return super().get_queryset()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        chats = None
        return context

def index(request):
    return render(request, 'chats/index.html')