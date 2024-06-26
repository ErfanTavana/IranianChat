from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from IranianChat.utilities import convert_to_shamsi


class Chat(models.Model):
    participant1 = models.ForeignKey(User, related_name='chats_as_participant1', on_delete=models.CASCADE)
    participant2 = models.ForeignKey(User, related_name='chats_as_participant2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_message_time = models.DateTimeField(null=True, blank=True)

    @property
    def last_message_time_formatted(self):
        if self.last_message_time:
            return self.last_message_time.strftime("%Y-%m-%d %H:%M")
        return None

    def __str__(self):
        return f"{self.participant1.get_full_name()} - {self.participant2.get_full_name()}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    solar_time_stamp = models.CharField(max_length=40, blank=True, null=True)
    seen = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.timestamp:
            self.timestamp = timezone.now()
        if not self.solar_time_stamp:
            self.solar_time_stamp = convert_to_shamsi(self.timestamp.isoformat())
        if not self.pk:  # Check if the instance is being created
            self.chat.last_message_time = timezone.now()
            self.chat.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"
