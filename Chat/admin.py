from django.contrib import admin
from .models import Chat, Message

class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'participant1', 'participant2', 'created_at')
    search_fields = ('participant1__username', 'participant2__username', 'created_at')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'sender', 'content', 'timestamp')
    search_fields = ('sender__username', 'content', 'timestamp')

admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
