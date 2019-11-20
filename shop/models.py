from django.db import models

import twitter
import random
from bs4 import BeautifulSoup as bs
import commonmark

from users.models import CustomUser as CU

# Create your models here.

class Item(models.Model):
    title = models.CharField(max_length=100, unique=True)
    votes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    voted = models.CharField(max_length=10000, default='')
    project_link = models.URLField(blank=True)
    author = models.CharField(max_length=150)
    short_desc = models.CharField(max_length=500)
    language = models.CharField(max_length=150)
    long_desc = models.TextField(max_length=20000)
    url = models.CharField(max_length=200)
    # verified = models.BooleanField(default=False)
    
    @property
    def image(self):
        soup = bs(commonmark.commonmark(self.long_desc))
        img = soup.find('img', src=True, onload=False, onerror=False)
        if img:
            return img['src']
        else:
            return 'none'
    
    def update_url(self):
        title = self.title
        
        rm = '-_+={}[]|\\\'\":;?/>.<,!@#$%^&*()~`'
        for c in rm:
            title = title.replace(c, '')
        
        while '--' in title:
            title = title.replace('--', '-')
        
        self.url = 'https://jon.network/programming/{}/{}/'.format(self.pk, '-'.join(title.split(' ')))
        self.save()
    
    def tweet(self):
        keys = [
            'cN0MQI0Z83RFoMRrCS4fsEGgJ',
            'Kj6ogywq7UnwjvrzF1H4acEIAP2EZcWj8wjpuvmKJNZkOgIhJ8',
            '1158774312519778304-KAq6080qrkrwZpDusvanmH3qgCH263',
            'W6domXhqqgFxxYW5ATfxjW3YwufOGOK3xy3vbETqhMeaI'
            ]
        
        epic_words = [
            'EPIC',
            'AMAZING',
            'CRAZY',
            'LEDGENDARY',
            'AWESOME',
            'INCREDIBLE'
        ]

        api = twitter.Api(
            consumer_key=keys[0],
            consumer_secret=keys[1],
            access_token_key=keys[2],
            access_token_secret=keys[3]
        )
        
        message = '''
{} ({})

> {}

Post by: {}

#{} #code
'''.format(self.title, epic_words[random.randint(0, len(epic_words)-1)], self.url, self.short_desc[:100], self.author[:20], self.language)
        
        api.PostUpdate(message)
    
    def upvote(self, username):
        if username not in self.voted.split(';'):
            self.votes += 1
            self.voted += username + ';'
            self.save()
            a = CU.objects.get(username=self.author)
            a.rep += random.randint(9, 11)
            a.save()
            
    
    def downvote(self, username):
        if username not in self.voted.split(';'):
            self.votes -= 1
            self.voted += username + ';'
            self.save()
            a = CU.objects.get(username=self.author)
            a.rep -= random.randint(2, 4)
            a.save()
    
    def __str__(self):
        return self.title
        

class Comment(models.Model):
    author = models.CharField(max_length=150)
    body = models.TextField(max_length=2000)
    to_item = models.IntegerField()
    





