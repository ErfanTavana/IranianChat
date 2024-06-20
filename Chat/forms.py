from django import forms

from .models import Message


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['file', 'content', 'chat', 'sender', 'content']
