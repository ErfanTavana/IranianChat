from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.shortcuts import render
from Account.models import Profile
from .forms import FileUploadForm
from django.contrib.auth import logout
from django.utils import timezone

def index(request):
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
    chats = Chat.objects.filter(Q(participant1=request.user) | Q(participant2=request.user))

    # Check if the user is a participant in the chat
    if request.user not in [chat_detail.participant1, chat_detail.participant2]:
        return HttpResponseForbidden("You do not have access to view this chat.")

    profiles = Profile.objects.all()  # or any other logic to get profiles
    messages = Message.objects.filter(chat=chat_detail)

    return render(request, 'messenger.html',
                  {'chat_detail': chat_detail, 'chats': chats, 'profiles': profiles, 'messages': messages})


def file_upload_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = FileUploadForm()
    return render(request, 'file_upload.html', {'form': form})


from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings


@login_required
def get_messages(request, chat_id):
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
                                                                                                 'sender__profile__last_name')
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


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Message, Chat
import json

@csrf_exempt
@login_required
def send_message(request):
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

            return JsonResponse({'status': 'success', 'message': 'Message sent successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid data'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def logout_view(request):
    logout(request)
    return redirect('login_name')