#chats\models.py
from django.db import models

# Create your models here.
class Messange(models.Model):
    text = models.TextField(null=False, max_length=1000, verbose_name='Текст сообщения')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    sender = models.ForeignKey('users.CustomUser', on_delete=models.SET_DEFAULT, default='Пользователь не найден',
                                null=False, related_name='sent_mess', verbose_name='Отправитель')
    resepien = models.ForeignKey('users.CustomUser', on_delete=models.SET_DEFAULT, default='Пользователь не найден',
                                null=False, related_name='received_mess', verbose_name='Получатель')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-time_create', ]
    