from rest_framework import serializers
from chat.models import Chat,NewUser
from chat.views import get_user_contact


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        # fields = '__all__'
        fields = ('id','username','email','status','profile_pic','about')
        read_only = ('username','email','status','profile_pic','about')


class ContactSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value


class ChatSerializer(serializers.ModelSerializer):
    participants = ContactSerializer(many=True)

    class Meta:
        model = Chat
        fields = ('id', 'messages', 'participants')
        read_only = ('id')

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        chat = Chat()
        chat.save()
        for username in participants:
            contact = get_user_contact(username)
            chat.participants.add(contact)
        chat.save()
        return chat

