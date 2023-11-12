from django.contrib import admin
from .models import *
# Register your models here.

class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'time_create', 'is_readed', 'chat_id']
    list_display_links = ['id', 'sender', 'time_create',  ]
    list_filter = ['chat_id']


class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'type_chat']
    list_display_links = ['id', 'type_chat']

admin.site.register(Message, MessageAdmin)
admin.site.register(Chat, ChatAdmin)