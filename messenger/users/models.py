#users\models.py
from collections.abc import Iterable
from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.

class CustomUser(AbstractUser):

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'user_id': self.pk})
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class UserInfo(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='user_info', verbose_name='user_info')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None, blank=True, null=True, verbose_name='Фото')
    about_me = models.TextField(blank=True, null=True)
