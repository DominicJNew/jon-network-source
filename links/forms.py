from django import forms

class LinkForm(forms.Form):
    url = forms.URLField(label='URL', max_length=200)