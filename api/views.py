from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from chatroom.models import Chat

def get_chats(request):
    had = int(request.GET.get('had'))
    chats = list(Chat.objects.filter(channel='').values('body', 'sender', 'time_sent'))
    return JsonResponse({
        'chats': chats[had:],
        'num_chats': len(chats),
    })
    
def csrf_token(request):
    return JsonResponse({
        'token': get_token(),
    })