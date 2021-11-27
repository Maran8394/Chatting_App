from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username,password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username,password, **other_fields)

    def create_user(self, email, username,password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):

    STATUS = [
        ("Online","Online"),
        ("Away","Away"),
        ("Busy","Busy"),
        ("Offline","Offline"),

    ]

    username = models.CharField(max_length=150, unique=True,null=True)
    email = models.EmailField(unique=True,null=True, max_length=250)
    status = models.CharField(choices=STATUS,max_length=8,default="Online")
    profile_pic = models.ImageField(upload_to="profile_pics/",default="profile_pics/dummyImage.jpg")
    login_status = models.BooleanField(null=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="friends", null=True)
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