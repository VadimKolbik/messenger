from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView

from .forms import CustomUserCreationForm, CustomUserChangeForm, LoginUserForm
from .models import *
from chats.models import Chat

# Create your views here.
def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('chats:all_chats'))
    else:
        form = LoginUserForm()
    
    return render(request, 'users/login.html', {'form': form})

def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect(reverse('users:login'))
    else:
        return render(request, 'users/logout.html')

class ProfileView(DetailView):
    model = CustomUser
    template_name = 'users/other_user.html'
    context_object_name = 'user'
    pk_url_kwarg = 'user_id'
    
    def get_template_names(self):
        if self.request.user.id == self.kwargs['user_id']:
            return ('users/profile.html', )
        else:
            return ('users/other_user.html', )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chat_id'] = Chat.objects.filter(members__in=[self.request.user.id, self.kwargs['user_id']]).distinct()[0].id
        return context


class PeopleView(ListView):
    '''All signup people'''
    model = CustomUser
    template_name = 'users/people.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Люди'
        return context