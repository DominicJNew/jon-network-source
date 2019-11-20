from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from .forms import LinkForm
from .models import Link

import random

import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse

def get_page_title(url):
    html = requests.get(url).text
    return bs(html, 'html.parser').title.string

# Create your views here.

def index(request):
    catagories = list(set([link.catagory for link in Link.objects.all()]))
    random.shuffle(catagories)
    return render(request, 'links/index.html', {'catagories': catagories, 'num_links': len(Link.objects.all())})

def link_share(request, catagory):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            
            try:
                page_title = get_page_title(url)
            except:
                return HttpResponse('<h1>The URL is invalid. Redirecting you...</h1><script>setTimeout(function(){{window.location.href="/links/{}/"}}, 2000)</script>'.format(catagory))
            
            if 'porn' in page_title.lower() or 'porn' in url:
                return HttpResponse('<h1>The URL is suspected for inapproprate content. DO NOT DO IT (if it was.) Redirecting you...</h1><script>setTimeout(function(){{window.location.href="/links/{}/"}}, 3000)</script>'.format(catagory))
            
            link = Link(
                url=url,
                title=page_title[:75] + '...' if len(page_title) > 80 else page_title,
                catagory=catagory.lower(),
                domain=urlparse(url).hostname,
            )
            link.save()
            
    links = list(Link.objects.filter(catagory=catagory))[::-1]

    if catagory != catagory.lower():
        return HttpResponseRedirect('/links/{}/'.format(catagory.lower()))
    
    return render(request, 'links/main.html', {'links': links, 'form': LinkForm(), 'catagory': catagory})
    