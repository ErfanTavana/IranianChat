from django.urls import path

from .views import index, chat_details, file_upload_view

# urls.py

urlpatterns = [
    path('', index, name='index_name'),
    path('chat_details/<int:id>', chat_details, name='chat_details_name'),
    path('upload/', file_upload_view, name='file_upload'),
]
