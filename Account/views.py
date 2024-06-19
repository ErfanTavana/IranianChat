from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login

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

