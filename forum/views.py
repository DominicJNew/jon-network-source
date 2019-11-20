from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Forum, Reply

from django.template import Template, Context

import markdown
import re
import json

# Create your views here.

def index(request):
    a = Forum.objects.all()
    return render(request, 'forum/forum.html', {'items': a[::-1]})

def add_item(request):
    if request.method == 'POST' and request.user.is_authenticated:
        item = Forum()
        item.title = request.POST.get('question', None)
        item.sender = request.user.username
        item.body = request.POST.get('body', None)
        item.language = request.POST.get('language', None)
        item.voted = request.user.username + ';'
        item.save()
        item.update_url()
        return render(request, 'forum/success.html', {'title': item.title})
        
    elif not request.user.is_authenticated:
        return HttpResponseRedirect('https://jon.network/acct/login')
        
    return render(request, 'forum/add_item.html')

def item_page(request, k, t):
    scroll_to_bottom = False
    if request.method == 'POST':
        try:
            replyVote = json.loads(request.body.decode('utf-8'))['intent'] == 'replyVote'
        except:
            replyVote = False
        
        if request.POST.get('intent') == 'vote':
            vote_data = request.POST.get('vote')
            key = vote_data[1:] 
            vote = vote_data[:1]
    
            item = Forum.objects.get(pk=int(key))
            if vote == 'u':
                item.upvote(request.user.username)
            else:
                item.downvote(request.user.username)
        
        elif replyVote:
            vote_data = json.loads(request.body.decode('utf-8'))['vote']
            key = vote_data[1:] 
            vote = vote_data[:1]
    
            reply = Reply.objects.get(pk=int(key))
            if vote == 'u':
                reply.upvote(request.user.username)
            else:
                reply.downvote(request.user.username)
            
            return HttpResponse(reply.votes)

                
        elif request.POST.get('intent') == 'reply':
            r = Reply()
            r.body = request.POST.get('body')
            r.sender = request.user.username
            r.post_id = request.POST.get('post_id')
            r.voted = '{};'.format(request.user.username)
            r.save()
            scroll_to_bottom = True
    
    item = Forum.objects.get(pk=int(k))

    item.views += 1
    item.save()

    return render(request, 'forum/post.html', {'item': item, 'replies': Reply.objects.filter(post_id=str(item.pk)).order_by('-votes'), 'scroll_to_bottom': scroll_to_bottom})

