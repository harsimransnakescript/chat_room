
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=30, blank=True, null=True)
    mobile = models.CharField(max_length=17, blank=False, null=False )
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    upload_to = models.DateTimeField(auto_now=True)
    roomName = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.fullname
    

class Room(models.Model):
    
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
