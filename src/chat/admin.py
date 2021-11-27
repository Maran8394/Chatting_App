from django.contrib import admin
from .models import Message, Contact, Chat
from . models import NewUser
from django.utils.translation import ugettext_lazy as _




admin.site.register(NewUser)

admin.site.register(Message)
admin.site.register(Contact)
admin.site.register(Chat)

