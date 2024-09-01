# users/forms.py
from typing import Any, Mapping
from django import forms
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList
from .models import Message, GalleryMessage


class MultipleFileInput(forms.ClearableFileInput):
    '''Для загрузки нескольких файлов в одном поле'''
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    '''Для загрузки нескольких файлов в одном поле'''
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class MessageForm(forms.ModelForm):
    list_img = MultipleFileField(label='Select files', required=False)

    class Meta:
        model = Message
        fields = ['text', 'list_img']
        labels = {'text': '', }
        widgets = {
            'text': forms.TextInput(attrs={'type': 'text', 'class': "form-control", 'aria-describedby': 'inputGroup-sizing-sm'}),
        }

class CreateGroupChatForm(forms.Form):
    chat_title = forms.CharField(max_length=100, required=True)
    users = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)