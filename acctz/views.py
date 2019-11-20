from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from users.models import CustomUser as CU
from shop.models import Item
import hashlib

from social_django.models import UserSocialAuth

def user_profile(request, un):
    user_prof = CU.objects.get(username=un)
    items = Item.objects.filter(author=un)
    
    return render(request, 'account.html', {'user_prof': user_prof, 'items': enumerate(items[::-1]), 'there_are_items': len(items) > 0})

def four_oh_four(request, forohfor):
    return HttpResponse("<head><title>202+202 - Jon's Network</title></head><h1>202+202</h1>That's an error. Please note that all urls are <strong>case-sensitve</strong>.", status=404)
    
def hacked(request):
    return HttpResponse('<h1>>:/</h1>Really. Me? Little old me?! You chose ME to hack?? Really. I don\'t belive it!! I want you to know you are a BAD PERSON!!! Rawr.')