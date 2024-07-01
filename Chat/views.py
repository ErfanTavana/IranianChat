import os

from django.conf import settings
from django.db.models import Q
from django.http import FileResponse
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from Account.models import Profile
from Chat.models import Message  # Assuming Message model is in Chat.models
from .models import Chat


def index(request):
    if not request.user.is_authenticated:
        return redirect('login_name')

    profiles = Profile.objects.exclude(user=request.user)  # حذف پروفایل فعلی کاربر از لیست
    chats = Chat.objects.filter(Q(participant1=request.user) | Q(participant2=request.user)).order_by(
        'last_message_time')

    for profile in profiles:
        # بررسی وجود چت بین کاربر فعلی و پروفایل‌های دیگر
        existing_chat = Chat.objects.filter(
            Q(participant1=request.user, participant2=profile.user) |
            Q(participant1=profile.user, participant2=request.user)
        ).first()

        if not existing_chat:
            # اگر چت بین این دو کاربر وجود ندارد، آن را ایجاد کنید
            chat_create, created = Chat.objects.get_or_create(
                participant1=request.user,
                participant2=profile.user
            )
    # بازگرداندن پروفایل‌ها و چت‌های موجود به قالب
    return render(request, 'chat_blank.html', {'profiles': profiles, 'chats': chats})


def chat_details(request, id):
    if not request.user.is_authenticated:
        return redirect('login_name')

    profiles = Profile.objects.exclude(user=request.user)  # حذف پروفایل فعلی کاربر از لیست
    chats = Chat.objects.filter(Q(participant1=request.user) | Q(participant2=request.user))

    for profile in profiles:
        # بررسی وجود چت بین کاربر فعلی و پروفایل‌های دیگر
        existing_chat = Chat.objects.filter(
            Q(participant1=request.user, participant2=profile.user) |
            Q(participant1=profile.user, participant2=request.user)
        ).first()

        if not existing_chat:
            # اگر چت بین این دو کاربر وجود ندارد، آن را ایجاد کنید
            chat_create, created = Chat.objects.get_or_create(
                participant1=request.user,
                participant2=profile.user
            )
    chat_detail = get_object_or_404(Chat, id=id)
    chats = Chat.objects.filter(Q(participant1=request.user) | Q(participant2=request.user)).order_by(
        'last_message_time')

    # Check if the user is a participant in the chat
    if request.user not in [chat_detail.participant1, chat_detail.participant2]:
        return HttpResponseForbidden("You do not have access to view this chat.")

    profiles = Profile.objects.all()  # or any other logic to get profiles
    messages = Message.objects.filter(chat=chat_detail).order_by('-timestamp')

    return render(request, 'messenger.html',
                  {'chat_detail': chat_detail, 'chats': chats, 'profiles': profiles, 'messages': messages})


def get_messages(request, chat_id):
    if not request.user.is_authenticated:
        return redirect('login_name')
    chat_detail = get_object_or_404(Chat, id=chat_id)

    # Check if the user is a participant in the chat
    if request.user not in [chat_detail.participant1, chat_detail.participant2]:
        return HttpResponseForbidden("You do not have access to view this chat.")

    messages = Message.objects.filter(chat=chat_detail).select_related('sender__profile').values('id',
                                                                                                 'sender__username',
                                                                                                 'content', 'timestamp',
                                                                                                 'solar_time_stamp',
                                                                                                 'file',
                                                                                                 'sender__profile__profile_picture',
                                                                                                 'sender__profile__first_name',
                                                                                                 'sender__profile__last_name',
                                                                                                 'seen','chat_id').order_by('-timestamp')
    messages_list = list(messages)
    for message in messages_list:
        message['timestamp'] = message['solar_time_stamp']
        message['file_url'] = ''
        message['file_name'] = ''
        message['file_size'] = ''
        if message['file']:
            message_instance = Message.objects.get(id=message['id'])
            if message_instance.file:
                message['file_url'] = message_instance.file.url
                message['file_name'] = message_instance.file.name
                message['file_size'] = message_instance.file.size

        if message['sender__profile__profile_picture']:
            message['profile_picture_url'] = settings.MEDIA_URL + message['sender__profile__profile_picture']
        else:
            message['profile_picture_url'] = settings.STATIC_URL + 'path/to/default/avatar.jpg'

    return JsonResponse(messages_list, safe=False)


@csrf_exempt
def send_message(request):
    if not request.user.is_authenticated:
        return redirect('login_name')
    if request.method == "POST":
        chat_id = request.POST.get('chat_id')
        sender_id = request.POST.get('sender_id')
        content = request.POST.get('content')
        file = request.FILES.get('file')

        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid chat ID'})

        if chat_id and (content or file):
            message = Message(
                chat=chat,
                sender_id=sender_id,
                content=content,
                timestamp=timezone.now()
            )
            if file:
                message.file = file
            message.save()
            chat.last_message_time = timezone.now()
            chat.save()

            return JsonResponse({'status': 'success', 'message': 'Message sent successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid data'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def serve_chat_file(request, file_name):
    print("Request to serve file:", file_name)
    if not request.user.is_authenticated:
        return redirect('login_name')
    # پیدا کردن پیام حاوی فایل
    message = get_object_or_404(Message, file='chat_files/' + file_name)

    # پیدا کردن چت مرتبط
    chat = message.chat

    # بررسی اینکه آیا کاربر یکی از شرکت‌کنندگان در چت است یا خیر
    if request.user.id != chat.participant1.id and request.user.id != chat.participant2.id and not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to access this file.")

    # پیدا کردن مسیر فایل
    file_path = os.path.join(settings.MEDIA_ROOT, 'chat_files', file_name)

    # بازگرداندن فایل به عنوان پاسخ
    return FileResponse(open(file_path, 'rb'))


@csrf_exempt
def seen_messages(request):
    print("seen message", request.user.username)
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'شما به این چت دسترسی ندارید'})

    if request.method == "POST":
        chat_id = request.POST.get('chat_id')
        chat = get_object_or_404(Chat, id=chat_id)

        if chat.participant1.id != request.user.id and chat.participant2.id != request.user.id:
            return JsonResponse({'status': 'error', 'message': 'شما به این چت دسترسی ندارید'})

        message_ids = request.POST.get('message_ids')
        message_ids_list = message_ids.split(',')

        receiver = chat.participant1 if chat.participant1.id != request.user.id else chat.participant2

        messages = Message.objects.filter(id__in=message_ids_list, chat=chat, sender=receiver)

        for message in messages:
            message.seen = True
            message.save()

        return JsonResponse({'status': 'success', 'message': 'بازدید از پیام‌ها ثبت شد'})
    return JsonResponse({'status': 'error', 'message': 'درخواست نامعتبر است'}, status=400)
