from django.urls import path

from .views import index, chat_details

# urls.py

urlpatterns = [
    path('', index, name='index_name'),
    path('chat_details/<int:id>', chat_details, name='chat_details_name')
]
