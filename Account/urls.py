from django.urls import path

from .views import login, logout_view, register

urlpatterns = [
    path('register/', register, name='register_name'),
    path('login/', login, name='login_name'),
    path('logout/', logout_view, name='logout_name'),
]
