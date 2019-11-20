from django.urls import path
import scriptlytics.views as views

urlpatterns = [
    path('<int:software_id>/image/', views.scriptlytics_image),
    path('<int:software_id>/', views.graph),
    path('hit/', views.hit),
    path('new/', views.new),
    path('get/', views.get),
]