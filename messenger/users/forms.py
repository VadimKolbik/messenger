# users/forms.py
from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from .models import CustomUser, UserInfo

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторить пароль', widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

class CustomUserChangeForm(UserChangeForm):
    username = forms.CharField(disabled=True, label='Логин')
    email = forms.CharField(disabled=True, label='E-mail')
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

class UserInfoForm(forms.ModelForm):
    photo = forms.ImageField(label='Фото')
    about_me = forms.CharField(label='О себе', required=False)

    class Meta:
        model = UserInfo
        fields = ['photo', 'about_me']


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput())
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput())
    new_password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput())