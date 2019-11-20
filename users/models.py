# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
import hashlib

class CustomUser(AbstractUser):
    # add additional fields in here
    bio = models.CharField(max_length=1500, default="", blank=True, null=True)
    rep = models.IntegerField(default=0)
    github = models.CharField(max_length=100, default="", blank=True, null=True)
    twitter = models.CharField(max_length=100, default="", blank=True, null=True)
    facebook = models.CharField(max_length=100, default="", blank=True, null=True)
    linkedin = models.CharField(max_length=100, default="", blank=True, null=True)
    instagram = models.CharField(max_length=100, default="", blank=True, null=True)
    personal = models.CharField(max_length=100, default="", blank=True, null=True)
    coin_address_type = models.CharField(max_length=100, default="", blank=True, null=True)
    coin_address = models.CharField(max_length=100, default="", blank=True, null=True)
    
    @property
    def gravatar(self):
        email_hash = hashlib.md5(str(self.email).encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}/?d=identicon&r=PG'.format(email_hash)
    
    def __str__(self):
        return self.email