from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.db.models import Count

from .forms import *
from .models import *
from chats.models import Chat
from chats.views import LoginRequiredMixin


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'
    extra_context = {
        'title': 'Регистрация'
    }
    success_url = reverse_lazy('users:login')
    
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        UserInfo(user=form.instance).save()
        return HttpResponseRedirect(self.get_success_url())


class ProfileView(DetailView):
    model = CustomUser
    template_name = 'users/other_user.html'
    context_object_name = 'current_user'
    pk_url_kwarg = 'user_id'

    def get_queryset(self) -> QuerySet[Any]:
        return CustomUser.objects.filter(pk=self.kwargs['user_id']).select_related('user_info')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chat'] = Chat.objects.filter(members__in=[self.request.user.id, self.kwargs['user_id']], type_chat=Chat.ChatType.DIALOG).annotate(c=Count('members')).filter(c=2).first()
        context['active_page'] = 1 if self.request.user.id == self.kwargs['user_id'] else 3
        return context
    
    def get_template_names(self):
        if self.request.user.id == self.kwargs['user_id']:
            return ('users/profile.html', )
        else:
            return ('users/other_user.html', )


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile, create = UserInfo.objects.get_or_create(user_id=request.user.id)
        user_info_form = UserInfoForm(instance=profile)
        data = {'user_info_form': user_info_form}
        return render(request, 'users/edit_profile.html', data)

    def post(self, request, *args, **kwargs):
        profile, create = UserInfo.objects.get_or_create(user_id=request.user.id)
        user_info_form = UserInfoForm(request.POST, request.FILES, instance=profile)
        if user_info_form.is_valid():
            user_info_form.save()
            return redirect('users:edit_profile')
        
        data = {'user_info_form': user_info_form}
        return render(request, 'users/edit_profile.html', data)

class PeopleView(ListView):
    '''All signup people'''
    model = CustomUser
    template_name = 'users/people.html'
    context_object_name = 'users'

    def get_queryset(self) -> QuerySet[Any]:
        return CustomUser.objects.all().select_related('user_info')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Люди'
        context['active_page'] = 3
        return context


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'
    extra_context = {'title': 'Смена пароля'}

class UserPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'
    extra_context = {'title': 'Пароль изменён'}