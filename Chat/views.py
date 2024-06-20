from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from Account.models import Profile
from Chat.models import Chat, Message


def index(request):
    if not request.user.is_authenticated:
        return redirect('login_name')
    profiles = Profile.objects.all()
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
