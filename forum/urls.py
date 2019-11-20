from django.contrib import admin
from django.urls import include, path
import forum.views as forum_views

urlpatterns = [
    path('', forum_views.index),
    path('post/<str:k>/<str:t>/', forum_views.item_page),
    path('make-post/', forum_views.add_item),
]
