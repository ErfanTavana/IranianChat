import random
import string

import ghasedakpack
from django.contrib.auth import authenticate, login as auth_login

from .models import Profile


def generate_random_password():
    return ''.join(random.choices(string.digits, k=6))


def register(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            return render(request, 'register.html')
        if request.method == 'POST':
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            profile_picture = request.FILES.get('profile_picture')  # اصلاح به Files
            responsibility = request.POST.get('responsibility')
            phone_number = username
            try:
                user = User.objects.get(username=username)
                return render(request, 'register.html', {'error': 'نام کاربری از قبل وجود دارد'})
            except User.DoesNotExist:
                password_random = generate_random_password()
                user = User.objects.create_user(username=username, password=password_random)
                Profile.objects.create(user_id=user.id, first_name=first_name, last_name=last_name,
                                       profile_picture=profile_picture, responsibility=responsibility,
                                       phone_number=phone_number)
                print(password_random)
                # ارسال کد تایید از طریق سرویس پیامکی
                sms = ghasedakpack.Ghasedak("1feaff6b0fb9ab14d5f1b9acc9fcad839699b313816e3001e128cef8e6271850")
                print(sms.verification({'receptor': f'{phone_number}', 'type': '1', 'template': 'NewEmployeePassword',
                                        'param1': f'{phone_number}', 'param2': f'{password_random}'}))
                return render(request, 'register.html', {'ok': 'کارمند با موفقیت اضافه شد'})
    else:
        if request.user.is_authenticated:
            return redirect('index_name')
        else:
            return redirect('login_name')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index_name')  # صفحه‌ای که می‌خواهید پس از ورود موفقیت‌آمیز کاربر او را به آن هدایت کنید
        else:
            error_message = "نام کاربری یا رمز ورود اشتباه است."
            return render(request, 'login.html', {
                'error_message': error_message,
                'username_error': True,
                'password_error': True,
                'username': username,
            })
    return render(request, 'login.html')


from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect


def password_change(request):
    if not request.user.is_authenticated:
        return redirect('login_name')
    context = {}

    if request.method == 'GET':
        return render(request, 'password_change.html', context)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        new_password_confirm = request.POST.get('new_password_confirm')

        if new_password != new_password_confirm:
            context['error'] = "رمز عبور و تکرار آن یکسان نیستند."
            return render(request, 'password_change.html', context)

        if not new_password or not new_password_confirm:
            context['error'] = "هر دو فیلد رمز عبور باید پر شوند."
            return render(request, 'password_change.html', context)

        user = request.user
        user.set_password(new_password)
        user.save()

        # Delete all sessions for the user
        sessions = Session.objects.all()
        deleted_sessions = 0

        for session in sessions:
            data = session.get_decoded()
            if str(user.pk) == str(data.get('_auth_user_id')):
                print(f'Deleting session: {session.session_key}')
                session.delete()
                deleted_sessions += 1

        # Logout the user
        logout(request)

        return redirect('login_name')

    return render(request, 'password_change.html', context)


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('login_name')

    user = request.user
    sessions = Session.objects.all()
    deleted_sessions = 0

    for session in sessions:
        data = session.get_decoded()
        if str(user.pk) == str(data.get('_auth_user_id')):
            session.delete()
            deleted_sessions += 1

    logout(request)
    return redirect('login_name')
