from django.http import HttpResponse as HttpRes
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
import json

@login_required
def index(request):
    return render(request, 'vids.html')
