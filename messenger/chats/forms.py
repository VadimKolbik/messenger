# users/forms.py
from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text', ]
        labels = {'text': '', }
        widgets = {
            'text': forms.Textarea(attrs={'cols': 65, 'rows': 1}),
        }