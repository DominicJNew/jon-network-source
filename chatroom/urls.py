from django.urls import path
from .views import *

urlpatterns = [
    path('', chatroom_index),
    path('send/', upload_chat), 
    path('chats/', get_chats), 
    path('<str:c>/', chatroom),
    path('<str:c>/image/', chat_image),
    path('embed/how-to/', how_to_embed),
]