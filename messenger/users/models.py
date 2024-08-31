#users\models.py
from collections.abc import Iterable
from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser, AnonymousUser
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# Create your models here.

class CustomUser(AbstractUser):
    last_online = models.DateTimeField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'user_id': self.pk})
    
    def is_online(self):
        if self.last_online:
            return (timezone.now() - self.last_online) < timezone.timedelta(minutes=15)
        return False
    
    def get_online_info(self):
        if self.is_online():
            return _('Online')
        if self.last_online:
            return _(f'Last visit {self.last_online}')
        return _('Unknown')
    

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class UserInfo(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='user_info', verbose_name='user_info')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None, blank=True, null=True, verbose_name='Фото')
    about_me = models.TextField(blank=True, null=True)
    friends = models.ManyToManyField('self', verbose_name='Друзья')

    def __str__(self):
        return f'Info about user {self.user}'
    
    class Meta:
        verbose_name = 'Информация о пользователе'
        verbose_name_plural = 'Информация о пользователях'