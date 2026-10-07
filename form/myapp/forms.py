from django import forms
from .models import MyappStudent
class Personal(forms.ModelForm):
        class Meta:
            model=MyappStudent
            fields = ['name','age','dob','phone','email']
        
        name = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs=
        {
            "class":"info-box",
            "placeholder":"enter your name"
        }
        ))
        
        age = forms.IntegerField(widget=forms.TextInput(attrs=
        {
            "class":"info-box",
            "placeholder":"enter your age"

        }
        ))
        
        dob = forms.DateField(    widget=forms.TextInput(attrs=
        {
            "class":"info-box",
            "type": "date"
        }
        ))
        
        phone=forms.CharField(max_length=10,    widget=forms.TextInput(attrs=
        {
            "class":"info-box",
            "placeholder":"enter your phone number"

        }
        ))
        
        email = forms.CharField( max_length=254,    widget=forms.TextInput(attrs=
        {
            "class":"info-box",
            "placeholder":"enter your email id"

        }
        ))