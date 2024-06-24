from django.contrib.auth.models import User
from django.db import models
from django.templatetags.static import static


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')
    first_name = models.CharField(max_length=50, blank=True, verbose_name='نام')
    last_name = models.CharField(max_length=50, blank=True, verbose_name='نام خانوادگی')
    phone_number = models.CharField(max_length=15, blank=True, verbose_name='شماره تماس')

    bio = models.TextField(max_length=500, blank=True, verbose_name='بیوگرافی')
    birth_date = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True,
                                        verbose_name='عکس پروفایل', default='user.png')
    responsibility = models.CharField(max_length=100, blank=True, verbose_name='مسئولیت')

    def save(self, *args, **kwargs):
        if not self.profile_picture:
            self.profile_picture = 'user.png'
        self.user.first_name = self.first_name.strip()
        self.user.last_name = self.last_name.strip()
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
