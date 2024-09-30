from django import forms

class VideoForm(forms.Form):
    text = forms.CharField(max_length=255)
    image = forms.ImageField(required=False)