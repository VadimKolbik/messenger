from django.contrib import admin
from .models import *
# Register your models here.

class MessangeAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'resepien', 'time_create', ]
    list_display_links = ['id', 'sender', 'resepien', 'time_create',  ]


admin.site.register(Messange, MessangeAdmin)