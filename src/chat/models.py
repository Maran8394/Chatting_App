from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends", null=True)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username

class Message(models.Model):
    contact = models.ForeignKey(Contact, related_name='Messages', on_delete=models.CASCADE, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact.user.username

class Chat(models.Model):
    participants = models.ManyToManyField(Contact, related_name="chats")
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return "{}".format(self.pk)