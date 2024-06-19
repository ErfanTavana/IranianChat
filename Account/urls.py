from django.urls import path

from .views import login

# urls.py

urlpatterns = [
    path('login/', login, name='login_name')
]
