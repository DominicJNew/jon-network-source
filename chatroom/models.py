from django.db import models

# Create your models here.

class Chat(models.Model):
    body = models.CharField(max_length=250)
    sender = models.CharField(max_length=150)
    time_sent = models.CharField(max_length=100)
    channel = models.CharField(max_length=100, default='')