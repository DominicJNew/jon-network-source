from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404

from .models import Item, Comment
from users.models import CustomUser as CU

import commonmark
from django.template import Template, Context

import re # for sterilizer
import requests
from bs4 import BeautifulSoup
import random

# Create your views here.

def items(request):
    if request.GET.get('q', None):
        return search(request)
    items = []
    popular_langs = []
    languages = [item.language.lower() for item in Item.objects.all()]
    
    for lang in languages:
        if languages.count(lang) >= 2:
            popular_langs.append(lang.title())
    
    for item in Item.objects.all()[::-1]:
        if item.votes > -5:
            items.append(item)
        if len(items) >= 50: #max 50 items
            break
    
    py = list(filter(lambda item: item.language.lower() == 'python', items))
    js = list(filter(lambda item: item.language.lower() == 'javascript', items))
    cpp = list(filter(lambda item: item.language.lower() == 'c++' or item.language.lower() == 'cpp', items))
    
    return render(request, 'programming_projects.html', {
        'items': enumerate(items),
        'popular_langs': list(set(popular_langs)),
        'selected_lang': None,
        'py': enumerate(py), 
        'js': enumerate(js), 
        'cpp': enumerate(cpp),
        'q': None,
    })


def search(request):
    q = request.GET.get('q', '')
    items = []
    popular_langs = []
    languages = [item.language.lower() for item in Item.objects.all()]
    
    for lang in languages:
        if languages.count(lang) >= 2:
            popular_langs.append(lang.title())
    
    # # Search The Title, then the short desc., then author
    
    # Title
    for item in Item.objects.all().order_by('-views'):
        for word in item.title.lower().split(' '):
            if word in q.lower().split('+'):
                items.append(item)
    
    # Short Desc.
    for item in Item.objects.all().order_by('-views'):
        for word in item.short_desc.lower().split(' '):
            if (item not in items) and (word in q.lower().split('+')):
                items.append(item)
    
    # author
    for item in Item.objects.all().order_by('-views'):
        if (item not in items) and (item.author.lower() in q.lower().split('+')):
            items.append(item)
    
    q_match_user = CU.objects.filter(username__icontains=q)
    
    users = CU.objects.all().order_by('?')
    
    return render(request, 'programming_projects.html', {
        'items': enumerate(items),
        'num_items': len(items),
        'popular_langs': list(set(popular_langs)),
        'selected_lang': True,
        'q_match_user': q_match_user,
        'q': q.replace('+', ' '),
        'total_users': len(users),
        'random_user': users[0],
        'items_length': len(Item.objects.all()),
    })


def add_item(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/acct/login/?next={}'.format(request.build_absolute_uri()))
    if request.method == 'POST' and request.user.is_authenticated:
        item = Item()
        item.title = request.POST.get('title', None)
        item.author = request.user.username
        item.project_link = request.POST.get('link', None)
        item.short_desc = request.POST.get('short_desc', None)
        item.long_desc = request.POST.get('long_desc', None)
        item.language = request.POST.get('language', None)
        item.save()
        item.update_url()
        return HttpResponseRedirect(item.url)
        
    elif request.user.is_authenticated:
        return render(request, 'create_post.html')
    else:
        return HttpResponseRedirect('https://jon.network/acct/login')

    
def item_page(request, k, t):
    scroll_to_bottom = False
    if request.method == 'POST':
        if request.POST.get('intent') == 'vote':    
            vote_data = request.POST.get('vote')
            t = vote_data[1:] #title
            vote = vote_data[:1]
    
            item = Item.objects.get(title=t)
            if vote == 'u':
                item.upvote(request.user.username)
            else:
                item.downvote(request.user.username)
        elif request.POST.get('intent') == 'comment':
            comment = Comment()
            comment.body = request.POST.get('body')
            comment.author = request.user.username
            comment.to_item = request.POST.get('post_id')
            comment.save()
            scroll_to_bottom = True
        
    try:
        item = Item.objects.get(pk=k)
    except Item.DoesNotExist:
        return Http404
    
    items = Item.objects.all()[::-1]
    
    if item.author != request.user.username:
        item.views += 1
        item.save()
    
    author = CU.objects.get(username=item.author)
    comments = Comment.objects.filter(to_item=item.pk)
    
    return render(request, 'post.html', {
        'item': item, 
        'author': author, 
        'comments': comments, 
        'items': items[:3], 
        'scroll_to_bottom': scroll_to_bottom,
        'latest': items[0],
        'random': random.choice(items),
    })


def edit_item(request, k, t):
    item = Item.objects.get(pk=k)
    if request.method == 'POST' and (item.author == request.user.username):
        item.title = request.POST.get('title', None)
        item.project_link = request.POST.get('link', None)
        item.short_desc = request.POST.get('short_desc', None)
        item.long_desc = request.POST.get('long_desc', None)
        item.language = request.POST.get('language', None)
        item.save()
        item.update_url()
        return HttpResponseRedirect(item.url)
        
    if item.author == request.user.username or request.user.is_superuser:
        return render(request, 'edit_item.html', {'item': item})
    else:
        return HttpResponse('Wait What? You want to edit a post you didn\'t make? Hmmm... that is very unethical of you.', status=403)


def search_by_lang(request, langu):
    if request.method == 'POST':
        vote_data = request.POST.get('vote')
        t = vote_data[1:] #title
        vote = vote_data[:1]

        item = Item.objects.get(title=t)
        if vote == 'u':
            item.upvote(request.user.username)
        else:
            item.downvote(request.user.username)
        
    items = []
    popular_langs = []
    languages = [item.language.lower() for item in Item.objects.all()]
    
    for lang in languages:
        if languages.count(lang) >= 2:
            popular_langs.append(lang.capitalize())
    
    for item in Item.objects.all()[::-1]:
        if item.votes >= -5 and item.language.lower() == langu.lower():
            items.append(item)
            
        if len(items) >= 50: #max 50 items
            break
        
    return render(request, 'programming_projects.html', {'items': enumerate(items), 
                                                'popular_langs': list(set(popular_langs)),
                                                'selected_lang': langu,
                                                'q': None})
    

def import_from_github(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/acct/login/?next=/project/from-github/')
    if request.method == 'POST':
        url = request.POST.get('link')
        
        raw_github_url = url.replace('//github.com', '//raw.githubusercontent.com')
        raw_github_url += '/master/README.md' if url[-1] != '/' else 'master/README.md'
        
        response = requests.get(url)
        raw_response = requests.get(raw_github_url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
            
            item = Item()
            item.long_desc = raw_response.content.decode('utf-8')
            item.title = str(soup.title.string).split('/')[1]
            item.short_desc = request.POST.get('short_desc')
            item.project_link = url
            item.author = request.user.username
            item.language = request.POST.get('language', None)
            
            try:
                item.save()
            except IntegrityError:
                return HttpResponse('Someone already made that post!!!')    
            
            item.update_url()
            
            return HttpResponseRedirect('{}edit/'.format(item.url))
        else:
            return HttpResponse('Invalid GitHub URL. Please try again.')
    
    return render(request, 'import_from_github.html')

def generate_long_desc(thumbnail_url, video_id, short_desc):
    return '<img src="{}" style="display:none;"><iframe width="100%" height="500" src="https://www.youtube.com/embed/{}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe><br>{}'.format(thumbnail_url, video_id, short_desc)

def import_from_youtube(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/acct/login/?next=/programming/from-youtube/')
    if request.method == 'POST':
        url = request.POST.get('url')
        
        rm = ['https://', 'http://', 'www.']
        for r in rm:
            url = url.replace(r, '')
        yt_urls = ['youtube.com/watch?v=', 'youtu.be/']
        if yt_urls[0] in url or yt_urls[1] in url:
            video_id = url.replace(yt_urls[0], '') if yt_urls[0] in url else url.replace(yt_urls[1], '')
        else:
            return HttpResponse('Incorrect Link')
        thumbnail_url = 'https://img.youtube.com/vi/{}/hqdefault.jpg'.format(video_id)
        
        item = Item(
            title=request.POST.get('title'),
            short_desc=request.POST.get('short_desc'),
            language=request.POST.get('language'),
            long_desc=generate_long_desc(thumbnail_url, video_id, request.POST.get('short_desc')),
            author=request.user.username,
        )
        item.save()
        item.update_url()
        
        return HttpResponseRedirect('/programming-articles/')
    return render(request, 'import_from_youtube.html')
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   