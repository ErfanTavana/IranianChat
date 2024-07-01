from django.contrib import admin
from .models import Chat, Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'sender', 'timestamp', 'content', 'seen')
    list_filter = ('chat', 'sender', 'seen')
    search_fields = ('content', 'sender__username')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('chat', 'sender')

    def solar_time_stamp_display(self, obj):
        return obj.solar_time_stamp

    solar_time_stamp_display.short_description = 'Solar Time Stamp'

admin.site.register(Chat)
