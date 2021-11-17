from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message
from . views import get_last_10_messages, get_user_contact, get_current_chat

User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data): #4
    
        messages = get_last_10_messages(data['chatId'])
        
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)
        print("fetch_messages")

    def new_message(self, data):
        user_contact= get_user_contact(data['from'])
        print("User-contact",user_contact)
        message = Message.objects.create(
            contact=user_contact, 
            content=data['message'])
        
        current_chat = get_current_chat(data['chatId'])
        current_chat.messages.add(message)
        current_chat.save()
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        print("new_message")

        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        print("messages_to_json")

        return result

    def message_to_json(self, message): #2
        print("message_to_json")
        return {
            'id': message.id,
            'author': message.contact.user.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }
        


    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):  # 1st
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print("disconnect")


    def receive(self, text_data): #4
        data = json.loads(text_data)
        self.commands[data['command']](self, data)
        print("receive")
        

    def send_chat_message(self, message):     
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        print("send_chat_message")

    def send_message(self, message): #3
        self.send(text_data=json.dumps(message))
        print("send_message")


    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
        print("chat_message")


# messages_to_json
# send_message
# fetch_messages
# receive