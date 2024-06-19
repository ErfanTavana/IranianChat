from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')
    bio = models.TextField(max_length=500, blank=True, verbose_name='بیوگرافی')
    location = models.CharField(max_length=30, blank=True, verbose_name='مکان')
    birth_date = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    profile_picture = models.ImageField(upload_to=f'profile_pics/{user.username}_{user.id}', null=True, blank=True,
                                        verbose_name='عکس پروفایل')
    responsibility = models.CharField(max_length=100, blank=True, verbose_name='مسئولیت')

    def __str__(self):
        return self.user.username
