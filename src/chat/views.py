from django.shortcuts import get_object_or_404
from . models import Chat, Contact
from django.contrib.auth import get_user_model

User = get_user_model()

def get_last_10_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by('-timestamp').all()[:10]

def get_user_contact(username):
    # print("USERNAME", username)
    user_id = User.objects.get(username=username)
    user = Contact.objects.get_or_create(user_id=user_id.id)
    
    get_obj = Contact.objects.get(user=user_id)
    # user.friends.add(user_id)
    user = get_object_or_404(User, username=username)
    return get_object_or_404(Contact, user=user)

def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)
