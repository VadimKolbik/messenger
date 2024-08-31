from typing import Any
from django.db import models
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, View, DeleteView
from django.db.models import Q, Count, F, Max
from django.urls import reverse
from django.http import HttpResponseNotFound, Http404
from django.db.models import prefetch_related_objects
from .models import *
from users.models import UserInfo
from .forms import MessageForm, CreateGroupChatForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

class MyLoginRequiredView(LoginRequiredMixin):
    login_url = '/users/login'

class ChatsView(MyLoginRequiredView, ListView):
    '''All chats of user'''
    model = Chat
    template_name = 'chats/chats.html'
    context_object_name = 'chats'

    def get_queryset(self):
        #empty chats is have and filtering them
        #не получилось без сырого запроса сделать
        
        return Chat.objects.filter(members__in=[self.request.user.id]).\
                            annotate(last_message=Max('messages__id'), last_message_time_create=Max('messages__time_create')).\
                            order_by('-last_message_time_create').\
                            prefetch_related('members')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['active_page'] = 2
        return context


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
        context['active_page'] = 2
        context['title'] = 'Чат'
        context['form'] = MessageForm()
        if Chat.objects.get(pk=self.kwargs['chat_id']).type_chat == 'C':
            context['group_chat'] = Chat.objects.get(pk=self.kwargs['chat_id'])
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

class InfoAboutChatView(MyLoginRequiredView, DetailView):
    model = Chat
    template_name = 'chats/info_about_chat.html'
    context_object_name = 'chat'
    pk_url_kwarg = 'chat_id'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['friends'] = UserInfo.objects.get(user=self.request.user).friends.all
        context['active_page'] = 2
        return context

def chat_delete_view(request, chat_id):
    Chat.objects.get(pk=chat_id).delete()
    return redirect(reverse('chats:all_chats'))


class CreateChatView(MyLoginRequiredView, View):
    def get(self, request, user_id):
        chats = Chat.objects.filter(members__in=[request.user.id, user_id], type_chat=Chat.ChatType.DIALOG).annotate(c=Count('members')).filter(c=2)
        if chats.count() == 0:
            return render(request, 'chats/chat.html', {'form': MessageForm(), 'active_page': 2})
        else:
            chat = chats.first()
        return redirect(reverse('chats:chat', kwargs={'chat_id': chat.id}))
    
    def post(self, request, user_id):
        chats = Chat.objects.filter(members__in=[request.user.id, user_id], type_chat=Chat.ChatType.DIALOG).annotate(c=Count('members')).filter(c=2)
        if not chats:
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.chat_id = chat.pk
                message.sender = request.user
                message.save()
            return redirect(reverse('chats:chat', kwargs={'chat_id': chat.id}))
        else:
            return HttpResponseNotFound('<h1>Упс, что-то пошло не так...</h1>')

def users_for_groupchat(users):
    choices_users = [(user.user.pk, user.user.username) for user in users]
    return choices_users

class CreateGroupChatView(MyLoginRequiredView, View):
    def get(self, request, user_id):
        form = CreateGroupChatForm()
        form.fields['users'].choices = users_for_groupchat(request.user.user_info.friends.all())
        context = {'title': 'Создать групповой чат',
                   'form': form,
                   }
        return render(request, 'chats/create_group.html', context=context)

    def post(self, request, user_id):
        form = CreateGroupChatForm(request.POST)
        form.fields['users'].choices = users_for_groupchat(request.user.user_info.friends.all())
        if form.is_valid():
            title_chat, users = form.cleaned_data.values()
            new_group = Chat.objects.create(type_chat=Chat.ChatType.CHAT, title_chat=title_chat)
            new_group.members.add(get_user_model().objects.get(pk=request.user.pk))
            for user in users:
                new_group.members.add(get_user_model().objects.get(pk=int(user)))
            new_group.save()
            return redirect(reverse('chats:chat', kwargs={'chat_id': new_group.pk}))
        context = {'title': 'Создать групповой чат',
                   'form': form}
        return render(request, 'chats/create_group.html', context=context)

def index(request):
    return render(request, 'chats/index.html')

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Myyyyy Page not found</h1>')

def delete_user_from_group_chat(request, chat_id, user_id):
    group_chat = Chat.objects.get(pk=chat_id)
    group_chat.members.remove(user_id)
    return redirect(reverse('chats:info_about_chat', kwargs={'chat_id': chat_id}))

def add_user_in_group_chat(request, chat_id, user_id):
    group_chat = Chat.objects.get(pk=chat_id)
    group_chat.members.add(user_id)
    return redirect(reverse('chats:info_about_chat', kwargs={'chat_id': chat_id}))

