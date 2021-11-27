from django.http.response import HttpResponse
from rest_framework import permissions
from rest_framework.generics import (ListAPIView,RetrieveAPIView, CreateAPIView,DestroyAPIView,UpdateAPIView)
from rest_framework.response import Response
from chat.models import Chat,Contact, NewUser
from . serializers import ChatSerializer,UserDetailsSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView

User = get_user_model()
def get_user_contact(username):
    user = get_object_or_404(User, username = username)
    contact = get_object_or_404(Contact, user=user)
    return contact




class ChatListView(ListAPIView):
    serializer_class = ChatSerializer
    permisson_classes = (permissions.AllowAny,)

    def get_queryset(self):
        queryset = Chat.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            contact = get_user_contact(username)
            queryset = contact.chats.all()
        return queryset

class ChatDetailView(RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permisson_classes = (permissions.AllowAny,)

class ChatCreateView(CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permisson_classes = (permissions.IsAuthenticated,)

class ChatUpdateView(UpdateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permisson_classes = (permissions.IsAuthenticated,)

class ChatDeleteView(DestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permisson_classes = (permissions.IsAuthenticated,)
    
class UserView(APIView):
    def get(self, request):
        q = NewUser.objects.all()
        serializer = UserDetailsSerializer(q, many=True)
        return Response(serializer.data)




class UserViewPk(APIView):
    serializer_class = UserDetailsSerializer
    permisson_classes = (permissions.IsAdminUser,)

    def get(self,request,username):
        q = get_object_or_404(NewUser, username=username)
        serializer = UserDetailsSerializer(q)
        return Response(serializer.data)