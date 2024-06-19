from django.urls import path

from .views import index

# urls.py

urlpatterns = [
    path('', index, name='index_name')
]
