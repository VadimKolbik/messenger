#users\models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    pass

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class UserInfo(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, verbose_name='user')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    about_me = models.TextField(blank=True, null=True)
