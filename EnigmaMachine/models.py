from mainPage.models import User
from django.utils import timezone
from django.db import models





# Create your models here.

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messagesSent")
    recipient = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="MessagesReceived", blank=True, null=True)
    encryptedContent = models.TextField(blank=True)
    rotors = models.CharField(max_length=5,default="I,II,III")
    plugBoardSetting = models.CharField(blank=True,max_length=100)
    rotorPositions = models.CharField(max_length=3)
    timestamp = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)
    saved = models.BooleanField(default=False)
    public = models.BooleanField(default=True)



    def serialize(self):
        return {
            "id":self.id,
            "sender": self.sender.username,
            "recipient": self.recipient.username if self.recipient else None,
            "content": self.encryptedContent,
            "rotors": self.rotors,
            "plugSetting": self.plugBoardSetting,
            "position": self.rotorPositions,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "read": self.read,
            "saved": self.saved,
            "public": self.public,
        }


