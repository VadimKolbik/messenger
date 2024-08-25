#chats\models.py
from django.db import models
from .util import next_or_prev_in_order
from django.urls import reverse

# Create your models here.
class Message(models.Model):
    class MessageStatus(models.IntegerChoices):
        UNREAD = 0, 'Не прочитано'
        READ = 1, 'Прочитано'
    
    chat = models.ForeignKey('Chat', related_name='messages', verbose_name='Чат', on_delete=models.CASCADE)
    text = models.TextField(null=False, max_length=1000, verbose_name='Текст сообщения')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    sender = models.ForeignKey('users.CustomUser', on_delete=models.SET_DEFAULT, default=None,
                                related_name='sent_mess', verbose_name='Отправитель')
    is_readed = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), MessageStatus.choices)),
                                    default=MessageStatus.UNREAD, verbose_name='Статус')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-time_create', ]
    
    def __str__(self):
        return self.text
    
    def prev_by_time_create(self):
        filter_list = Message.objects.filter(chat_id=self.chat_id)
        return next_or_prev_in_order(self, True, filter_list)
    
    def next_by_time_create(self):
        filter_list = Message.objects.filter(chat_id=self.chat_id)
        return next_or_prev_in_order(self, False, filter_list)
    
    def reading_messages(self):
        Message.objects.filter(is_readed=Message.MessageStatus.UNREAD).\
                        update(is_readed=Message.MessageStatus.READ)


class Chat(models.Model):
    class ChatType(models.TextChoices):
        CHAT = 'C', 'Чат'
        DIALOG = 'D', 'Диалог'
    
    type_chat = models.CharField(max_length=1, choices=ChatType.choices, default=ChatType.DIALOG)
    members = models.ManyToManyField('users.CustomUser', related_name='chats', verbose_name='Участники')
    title_chat = models.CharField(max_length=100, blank=True, verbose_name='Название группового чата')
    # group_chat_photo = models.ImageField(upload_to="photos/chats/%Y/%m/%d/", default=None, blank=True, null=True, verbose_name='Фото')

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
    
    def __str__(self):
        try:
            return f'id={self.id} type={self.type_chat} time: {self.lastmessage().time_create}'
        except:
            return f'id={self.id} type={self.type_chat} time: '
    
    def get_absolute_url(self):
        return reverse('chats:chat', kwargs={'chat_id': self.pk})
    
    def lastmessage(self):
        try:
            return self.messages.order_by('-time_create')[0]
        except IndexError:
            return None