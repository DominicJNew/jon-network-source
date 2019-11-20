from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File
from users.models import CustomUser as CU
import random

class Img(models.Model):
    title = models.CharField(max_length=100)
    sender = models.CharField(max_length=150)
    cover = models.ImageField(upload_to='images/')
    body = models.CharField(max_length=1000, default='')
    votes = models.IntegerField(default=0)
    voted = models.CharField(max_length=10000, default='')
    impressions = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)

    def upvote(self, username):
        if username not in self.voted.split(';'):
            self.votes += 1
            self.voted += username + ';'
            self.save()
            a = CU.objects.get(username=self.sender)
            a.rep += random.randint(4, 6)
            a.save()
            
    
    def downvote(self, username):
        if username not in self.voted.split(';'):
            self.votes -= 1
            self.voted += username + ';'
            self.save()
            a = CU.objects.get(username=self.sender)
            a.rep -= random.randint(1, 2)
            a.save()
            
            
            