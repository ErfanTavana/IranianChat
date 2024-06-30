from django.urls import path

from .views import index, chat_details, get_messages, serve_chat_file, send_message

# urls.py

urlpatterns = [
    path('media/chat_files/<str:file_name>/', serve_chat_file, name='serve_chat_file'),

    path('', index, name='index_name'),
    path('chat_details/<int:id>', chat_details, name='chat_details_name'),
    path('chat/<int:chat_id>/messages/', get_messages, name='get_messages'),
    path('send_message/', send_message, name='send_message'),

]
