# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from Chat.views import serve_chat_file

urlpatterns = [
    path('media/chat_files/<str:file_name>/', serve_chat_file, name='serve_chat_file'),
    path('admin/', admin.site.urls),
    path('', include('Account.urls')),
    path('', include('Chat.urls')),
]

# Debug mode-specific URL patterns for serving media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
