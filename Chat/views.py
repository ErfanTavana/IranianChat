from django.db.models import Q
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from Account.models import Profile
from Chat.models import Chat
from .forms import FileUploadForm
from .models import Message


def index(request):
    if not request.user.is_authenticated:
        return redirect('login_name')
    profiles = Profile.objects.all()
    for profile in profiles:
        chat_create, get = Chat.objects.get_or_create(participant1_id=request.user.id, participant2_id=profile.id)
    chats = Chat.objects.filter(Q(participant1=request.user) | Q(participant2=request.user))
    return render(request, 'chat_blank.html', {'profiles': profiles, 'chats': chats})


def chat_details(request, id):
    if not request.user.is_authenticated:
        return redirect('login_name')

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
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def get_messages(request, chat_id):
    chat_detail = get_object_or_404(Chat, id=chat_id)

    # Check if the user is a participant in the chat
    if request.user not in [chat_detail.participant1, chat_detail.participant2]:
        return HttpResponseForbidden("You do not have access to view this chat.")

    messages = Message.objects.filter(chat=chat_detail).values('id', 'sender__username', 'content', 'timestamp', 'file')
    messages_list = list(messages)

    for message in messages_list:
        message['file_url'] = ''
        message['file_name'] = ''
        message['file_size'] = ''
        if message['file']:
            message_instance = Message.objects.get(id=message['id'])
            if message_instance.file:
                message['file_url'] = message_instance.file.url
                message['file_name'] = message_instance.file.name
                message['file_size'] = message_instance.file.size

    return JsonResponse(messages_list, safe=False)