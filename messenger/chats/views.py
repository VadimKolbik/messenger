from typing import Any
from django.db import models
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, View
from django.db.models import Q, Count, F, Max
from django.urls import reverse
from django.http import HttpResponseNotFound, Http404
from django.db.models import prefetch_related_objects
from .models import *
from .forms import MessageForm
from .queries import chats_filter

from django.contrib.auth.mixins import LoginRequiredMixin

class MyLoginRequiredView(LoginRequiredMixin):
    login_url = '/users/login'

menu = [
    {'title': 'Главная', 'url': 'home'},
    {'title': 'Регистрация', 'url': 'users:login'},
    {'title': 'Авторизация', 'url': 'users:login'},
]

class ChatsView(MyLoginRequiredView, ListView):
    '''All chats of users'''
    model = Chat
    template_name = 'chats/chats.html'
    context_object_name = 'chats'

    def get_queryset(self):
        #empty chats is have and filtering them
        #не получилось без сырого запроса сделать
        return Chat.objects.filter(members__in=[self.request.user.id]).\
                            annotate(c=Count('messages'), last_message=Max('messages__id'), last_message_time_create=Max('messages__time_create')).\
                            filter(c__gt=0).order_by('-last_message_time_create').\
                            prefetch_related('members')


class ChatView(MyLoginRequiredView, DetailView):
    '''Chat between 2 users'''
    model = Chat
    template_name = 'chats/chat.html'
    context_object_name = 'chat'
    pk_url_kwarg = 'chat_id'
 
    def get_object(self, queryset=None):
        # return Chat.objects.get(pk=self.kwargs['chat_id'])
        return Message.objects.filter(chat_id=self.kwargs['chat_id']).select_related('sender')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Чат'
        context['form'] = MessageForm()
        return context
    
    def get(self, request, chat_id):
        template_response = super().get(request, chat_id)
        
        #наличие пользователя в данном чате
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user in chat.members.all():
                chat.messages.filter(is_readed=Message.MessageStatus.UNREAD).exclude(sender=request.user).update(is_readed=True)
                return template_response
            else:
                raise Http404()
        except:
            raise Http404()

    def post(self, request, chat_id):
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.sender = request.user
            message.save()
        return redirect(reverse('chats:chat', kwargs={'chat_id': chat_id}))


class CreateChatView(MyLoginRequiredView, View):
    def get(self, request, user_id):
        chats = Chat.objects.filter(members__in=[request.user.id, user_id], type_chat=Chat.ChatType.DIALOG).annotate(c=Count('members')).filter(c=2)
        if chats.count() == 0:
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
        else:
            chat = chats.first()
        return redirect(reverse('chats:chat', kwargs={'chat_id': chat.id}))


def index(request):
    return render(request, 'chats/index.html')

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Myyyyy Page not found</h1>')