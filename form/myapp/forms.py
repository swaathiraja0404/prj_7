from django import forms
from .models import MyappStudent
class Personal(forms.Form):
    model=MyappStudent
    name = forms.CharField(max_length=100,
    widget=forms.TextInput(attrs=
    {
        "class":"info-box"
    }
    ))
    age = forms.IntegerField(widget=forms.TextInput(attrs=
    {
        "class":"info-box"
    }
    ))
    dod=forms.DateField(    widget=forms.TextInput(attrs=
    {
        "class":"info-box"
    }
    ))
    phone=forms.CharField(max_length=10,    widget=forms.TextInput(attrs=
    {
        "class":"info-box"
    }
    ))
    email = forms.CharField( max_length=254,    widget=forms.TextInput(attrs=
    {
        "class":"info-box"
    }
    ))