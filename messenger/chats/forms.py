# users/forms.py
from typing import Any, Mapping
from django import forms
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text', ]
        labels = {'text': '', }
        widgets = {
            'text': forms.Textarea(attrs={'cols': 65, 'rows': 1}),
        }

class CreateGroupChatForm(forms.Form):
    chat_title = forms.CharField(max_length=100, required=True)
    users = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)