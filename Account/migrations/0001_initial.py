# Generated by Django 5.0.6 on 2024-06-29 07:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50, verbose_name='نام')),
                ('last_name', models.CharField(blank=True, max_length=50, verbose_name='نام خانوادگی')),
                ('phone_number', models.CharField(blank=True, max_length=15, verbose_name='شماره تماس')),
                ('bio', models.TextField(blank=True, max_length=500, verbose_name='بیوگرافی')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')),
                ('profile_picture', models.ImageField(blank=True, default='user.png', null=True, upload_to='profile_pics/', verbose_name='عکس پروفایل')),
                ('responsibility', models.CharField(blank=True, max_length=100, verbose_name='مسئولیت')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
        ),
    ]