from django.urls import include, path
from .views import *

urlpatterns = [
    path('', all_images, name='img_home'),
    path('<int:k>/<str:t>/', image_page),
    path('next/<int:n>/', next_images),
    path('upload/', upload, name='upload_img'),
]