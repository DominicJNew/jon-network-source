from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import os
import datetime
import json
import requests
from PIL import Image, ImageDraw

from chatroom.models import Chat

def related_to(channel):
    word = channel[6:].replace('-', '+')
    words = json.loads(requests.get('https://api.datamuse.com/words?ml={}'.format(word)).content.decode('utf-8'))
    related = []
    while len(related) < 10:
        try:
            related.append(words[len(related)]['word'].replace(' ', '-'))
        except IndexError:
            return related
            
    return related if related else None


def chat_image(request, c):
    img = Image.new('RGB', (130 + len(c)*6, 20), (0))
    d = ImageDraw.Draw(img)
    d.text((0, 5), "CHAT/{} | Jon's Network".format(c), fill=(255, 255, 255))
    
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

def how_to_embed(request):
    return render(request, 'how_to_embed.html')

@csrf_exempt
def chatroom_index(request):
    return render(request, 'chatroom.html', {'chats': Chat.objects.filter(channel=''), 'channel': 'DevChat', 'related': related_to('/chat/code')})

@csrf_exempt
def chatroom(request, c):
    if c == '':
        channel = ''
    else:
        channel = '/chat/{}'.format(c)
    
    chats = Chat.objects.filter(channel=channel.lower())
    
    return render(request, 'chatroom.html', {'chats': chats, 'channel': channel, 'related': related_to(channel)})
    

@csrf_exempt
def get_chats(request):
    raw_json = json.loads(request.body.decode('utf-8'))
    b = raw_json['b']
    channel = '' if raw_json['channel'] == '/chat/' else raw_json['channel']
    chats = Chat.objects.filter(channel=channel.lower())
    
    if int(b) != len(chats):
        return render(request, 'chats.html', {'chats': chats[int(b):]})
    else:
        return HttpResponse('up to date')

@csrf_exempt
def upload_chat(request):
    if request.method == 'POST':
        raw_json = json.loads(request.body.decode('utf-8'))
        body = raw_json['body']
        
        if body != '':    
            c = Chat()
            c.body = body
            c.sender = request.user.username if request.user.is_authenticated else 'Anonymous'
            
            u = datetime.datetime.utcnow()
            
            c.time_sent = str(u.month) + '/' + str(u.day) + '@' + str(u.hour) + ':' + str(u.minute)
            c.channel = '' if raw_json['channel'] == '/chat/' else raw_json['channel'].lower()
            c.save()
        
        return HttpResponse('actual success')
    return HttpResponse('success')
