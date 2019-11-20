from django.shortcuts import render
from django.http import HttpResponseRedirect

from shop.models import Item
from image_upload.models import Img
from forum.models import Forum

from devkit.models import PageViewCounter

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'index/index.html')
    else:
        return HttpResponseRedirect('/programming-articles/')

def ide(request):
    view_counter = PageViewCounter.objects.get(pk=1)
    view_counter.page_views += 1
    view_counter.save()
    
    return render(request, 'ide/ide.html', {'views': view_counter.page_views})

def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    forum_posts = Forum.objects.all()[::-1]
    articles = Item.objects.all()[::-1][:20]
    images = Img.objects.all()[::-1][:20]
    
    return render(request, 'home.html')