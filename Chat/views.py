from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
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

    chat = get_object_or_404(Chat, id=id)

    # Check if the user is a participant in the chat
    if request.user not in [chat.participant1, chat.participant2]:
        return HttpResponseForbidden("You do not have access to view this chat.")

    profiles = Profile.objects.all()  # or any other logic to get profiles
    messages = Message.objects.filter(chat=chat)

    return render(request, 'messenger.html', {'chat': chat, 'profiles': profiles, 'messages': messages})