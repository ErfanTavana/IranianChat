from django.urls import path

from .views import login, logout_view

# urls.py

urlpatterns = [
    path('login/', login, name='login_name'),
    path('logout/', logout_view, name='logout_name'),

]
