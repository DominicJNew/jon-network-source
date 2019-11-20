from django.db import models

# Create your models here.

class Item(models.Model):
    message = models.CharField(max_length=1000)
    sender = models.CharField(max_length=200)
    
    def __str__(self):
        return '<b>' + str(sender) + '</b><br /><p>' + str(message) + '</p>'