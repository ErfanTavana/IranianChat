from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    participant1 = models.ForeignKey(User, related_name='chats_as_participant1', on_delete=models.CASCADE)
    participant2 = models.ForeignKey(User, related_name='chats_as_participant2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.participant1.username} and {self.participant2.username}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)  # New field to track seen status

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"