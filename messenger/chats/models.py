#chats\models.py
from django.db import models

# Create your models here.
class Message(models.Model):
    class MessageStatus(models.IntegerChoices):
        UNREAD = 0, 'Не прочитано'
        READ = 1, 'Прочитано'
    
    chat = models.ForeignKey('Chat', related_name='messages', verbose_name='Чат', on_delete=models.CASCADE)
    text = models.TextField(null=False, max_length=1000, verbose_name='Текст сообщения')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    sender = models.ForeignKey('users.CustomUser', on_delete=models.SET_DEFAULT, default='Пользователь не найден',
                                null=False, related_name='sent_mess', verbose_name='Отправитель')
    is_readed = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), MessageStatus.choices)),
                                    default=MessageStatus.UNREAD, verbose_name='Статус')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-time_create', ]
    
    def __str__(self):
        return self.text

class Chat(models.Model):
    class ChatType(models.TextChoices):
        CHAT = 'C', 'Чат'
        DIALOG = 'D', 'Диалог'
    
    type_chat = models.CharField(max_length=1, choices=ChatType.choices, default=ChatType.DIALOG)
    members = models.ManyToManyField('users.CustomUser', related_name='chats', verbose_name='Участники')

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
    
    def __str__(self):
        members = self.members.all()
        return f'id={self.id} type={self.type_chat} для {[m.username for m in members]}'