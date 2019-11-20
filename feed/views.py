from django.shortcuts import render

from image_upload.models import Img
from shop.models import Item
from forum.models import Forum

def trending(request):
    forum_posts = Forum.objects.all()[::-1]
    articles = Item.objects.all()[::-1][:20]
    images = Img.objects.all()[::-1][:20]
    
    return render(request, 'home.html')