# Generated by Django 3.2.6 on 2021-10-29 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_contact_friends'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='message',
            new_name='messages',
        ),
    ]