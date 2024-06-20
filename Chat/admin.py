from django.contrib import admin


class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'participant1', 'participant2', 'created_at')
    search_fields = ('participant1__username', 'participant2__username', 'created_at')
from django import forms
from .models import Message

class MessageAdminForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'

    class Media:
        js = ('js/upload_progress.js',)
# admin.py
from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    form = MessageAdminForm
    list_display = ('sender', 'chat', 'timestamp', 'seen')
    list_filter = ('sender', 'chat', 'seen', 'timestamp')
    search_fields = ('sender__username', 'content')
    date_hierarchy = 'timestamp'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('sender', 'chat')
        return queryset