from django.urls import path

from .views import login, logout_view, register, password_change

urlpatterns = [
    path('register/', register, name='register_name'),
    path('login/', login, name='login_name'),
    path('password_change/', password_change, name='password_change_name'),
    path('logout/', logout_view, name='logout_name'),
]
