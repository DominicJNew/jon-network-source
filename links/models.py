from django.db import models
import twitter
import random

from urllib.parse import urlparse

class Link(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=100)
    catagory = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    
    def tweet(self):
        keys = [
            'cN0MQI0Z83RFoMRrCS4fsEGgJ',
            'Kj6ogywq7UnwjvrzF1H4acEIAP2EZcWj8wjpuvmKJNZkOgIhJ8',
            '1158774312519778304-KAq6080qrkrwZpDusvanmH3qgCH263',
            'W6domXhqqgFxxYW5ATfxjW3YwufOGOK3xy3vbETqhMeaI'
            ]

        api = twitter.Api(
            consumer_key=keys[0],
            consumer_secret=keys[1],
            access_token_key=keys[2],
            access_token_secret=keys[3]
        )
        
        message = generate_msg(self.catagory, self.url)
        
        return api.PostUpdate(message)
    
    def update_domain(self):
        self.domain = urlparse(self.url).hostname
        self.save()
        
def generate_msg(catagory, link):
    links = list(Link.objects.all())
    num_links = len(links)
    return 'New Link: {}\nTotal Links: {}\nAll #{} links: https://jon.network/links/{}/\n~By L1nkB0t'.format(link, num_links, catagory, catagory)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    