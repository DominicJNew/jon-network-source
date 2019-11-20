from django import forms
from .models import Img

class ImgForm(forms.ModelForm):
    class Meta:
        model = Img
        fields = ['title', 'cover']