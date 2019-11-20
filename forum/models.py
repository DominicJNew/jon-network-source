from django.db import models
from users.models import CustomUser as CU

import random

# Create your models here.

bad_chars = '!@#$%^&*()_=+{[}]|\\\'\";:/?.,><`~'

class Forum(models.Model):
    title = models.CharField(max_length=75)
    
    votes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    voted = models.CharField(max_length=10000, null=True, default='')
    
    sender = models.CharField(max_length=150)
    body = models.CharField(max_length=500)
    language = models.CharField(max_length=150)
    url = models.CharField(max_length=200)
    
    def update_url(self):
        t = '-'.join(self.title.split(' '))
        for c in bad_chars:
            t = t.replace(c, '')
        self.url = 'https://jon.network/forum/post/' + str(self.pk) + '/' + t + '/'
        self.save()
    
    def upvote(self, username):
        if username not in self.voted.split(';') and username != self.sender:
            self.votes += 1
            self.voted += username + ';'
            self.save()
            a = CU.objects.get(username=self.author)
            a.rep += random.randint(9, 11)
            a.save()
            
    
    def downvote(self, username):
        if username not in self.voted.split(';') and username != self.sender:
            self.votes -= 1
            self.voted += username + ';'
            self.save()
            a = CU.objects.get(username=self.sender)
            a.rep -= random.randint(2, 4)
            a.save()
            

class Reply(models.Model):
    body = models.TextField()
    sender = models.CharField(max_length=150)
    post_id = models.CharField(max_length=1000)
    voted = models.CharField(max_length=10000, null=True, default='')
    votes = models.IntegerField(default=0)

    def upvote(self, username):
        if username not in self.voted.split(';') and username != self.sender:
            self.votes += 1
            self.voted += username + ';'
            self.save()
            a = CU.objects.get(username=self.sender)
            a.rep += random.randint(9, 11)
            a.save()
            
    
    def downvote(self, username):
        if username not in self.voted.split(';') and username != self.sender:
            self.votes -= 1
            self.voted += username + ';'
            self.save()
            a = CU.objects.get(username=self.sender)
            a.rep -= random.randint(2, 4)
            a.save()


        