from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.views.decorators.csrf import csrf_exempt
from .models import Img

import magic
from io import BytesIO
from PIL import Image
from django.core.files import File

import json

def compress(image):
    f = magic.Magic()
    im = Image.open(image)
    im = im.convert('RGB')
    im_io = BytesIO()
    
    im.save(im_io, 'JPEG', quality=70)
    
    new_image = File(im_io, name=image.name)
    return new_image

@csrf_exempt
def all_images(request):
    if request.method == 'POST' and request.user.is_authenticated:
        raw = json.loads(request.body.decode('utf-8'))['vote']
        if raw['intent'] == 'vote':
            img = Img.objects.get(pk=raw['pk'])
            if raw['vote'] == 'up':
                img.upvote(request.user.username)
            else:
                img.downvote(request.user.username)
        
        return HttpResponse(img.votes)

    imgs = Img.objects.all()[::-1][:5]

    for img in imgs:
        img.impressions += 1
        img.save()
    
    return render(request, 'img/all.html', {'imgs': enumerate(imgs)})


def image_page(request, k, t):
    img = Img.objects.get(pk=k)
    
    if img.sender != request.user.username:
        img.clicks += 1
        img.save()
    return render(request, 'img/page.html', {'img': img})


def next_images(request, n):
    try:
        imgs = Img.objects.all()[n-5:n]
        
        for img in imgs:
            img.impressions += 1
            img.save()
            
        return render(request, 'img/next_imgs.html', {'imgs': enumerate(imgs)})
    except:
        return HttpResponse('Invalid Request')

  
def upload(request):
    if request.method == 'POST':
        img = Img()
        img.sender = request.user.username if request.user.is_authenticated else 'Anonymous'
        
        img.cover = compress(request.FILES['cover'])
        
        img.title = request.POST.get('title')
        img.body = request.POST.get('body')
        img.save()
        return HttpResponseRedirect('https://jon.network/images/')
        
    return render(request, 'img/upload.html')
    
    
    