from django.urls import path
from .views import *

# included at api/

urlpatterns = [
    path('get-chats/', get_chats),
]