from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import CustomUser
from django.contrib.auth.models import AbstractUser
# Create your views here.

def user_index(request):
    return render(request, 'user_index.html', {'users': CustomUser.objects.all()})

def user_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('https://jon.network/user/' + str(request.user.username))
    else:
        return HttpResponseRedirect('https://jon.network/acct/login')
        
def edit_prof(request):
    if request.method == 'POST':
        user = CustomUser.objects.get(username=request.user.username)
        user.bio = request.POST.get('bio', None)
        user.github = request.POST.get('github', None)
        user.twitter = request.POST.get('twitter', None)
        user.facebook = request.POST.get('facebook', None)
        user.linkedin = request.POST.get('linkedin', None)
        user.instagram = request.POST.get('instagram', None)
        user.personal = request.POST.get('personal', None)
        user.coin_address_type = request.POST.get('coin_address_type', None)
        user.coin_address = request.POST.get('coin_address', None)
        user.save()
        return HttpResponseRedirect('https://jon.network/user/')
    elif request.user.is_authenticated:
        return render(request, 'edit_profile.html')
    else:
        return HttpResponseRedirect('https://jon.network/acct/login')

def email_addrs(request):
    if request.user.is_superuser:
        return render(request, 'emails.html', {'users': CustomUser.objects.all()})
    else:
        return HttpResponse('NO EMAIL FOR YOU, COME BACK, 2 WEEKS!')
    
    
    