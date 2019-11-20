from django.contrib import admin
from django.urls import include, path
import shop.views as shop_views

urlpatterns = [
    path('share/', shop_views.add_item),
    path('from-github/', shop_views.import_from_github),
    path('from-youtube/', shop_views.import_from_youtube),
    path('<int:k>/<str:t>/edit/', shop_views.edit_item),
    path('<int:k>/<str:t>/', shop_views.item_page),
]
