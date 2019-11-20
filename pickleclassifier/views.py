from django.shortcuts import render
from .forms import UploadFileForm
# from fastai.vision import *
# import torch

# Create your views here.

# model = torch.load('/home/raveivcs/backend/pickleclassifier/classifiers/export.pkl')

def index(request):
    # if request.method == 'POST':
    #     img = request.FILES
    #     pred = model(img)
    #     return render(request, 'classifier/results.html', {'pred': pred})
    return render(request, 'classifier/index.html')