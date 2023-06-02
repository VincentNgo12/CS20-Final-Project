# Generated by Django 4.2 on 2023-05-20 21:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('EnigmaMachine', '0002_message_public_alter_message_recipients'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='recipients',
        ),
        migrations.AddField(
            model_name='message',
            name='recipient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='MessagesReceived', to=settings.AUTH_USER_MODEL),
        ),
    ]