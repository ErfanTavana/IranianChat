from django.contrib import admin
from .models import Chat, Message
from django.contrib.auth.models import User

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_chat_participants', 'get_sender_full_name', 'timestamp', 'content', 'seen')
    list_filter = ('chat', 'sender', 'seen')
    search_fields = ('content', 'sender__username')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('chat', 'sender')

    def get_chat_participants(self, obj):
        return f"{obj.chat.participant1.get_full_name()} - {obj.chat.participant2.get_full_name()}"

    get_chat_participants.short_description = 'Chat Participants'

    def get_sender_full_name(self, obj):
        return obj.sender.get_full_name()

    get_sender_full_name.short_description = 'Sender Full Name'

    def solar_time_stamp_display(self, obj):
        return obj.solar_time_stamp

    solar_time_stamp_display.short_description = 'Solar Time Stamp'

admin.site.register(Chat)
