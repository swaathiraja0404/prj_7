from django import forms
from .models import MyappStudent,MyappStaff
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

class StaffPersonal(forms.ModelForm):
            class Meta:
                model=MyappStaff
                fields = ['name','age','dob','phone','email','department']
        
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
            
            department = forms.ChoiceField(choices=[
                    ('', 'Select Department'),
                    ('IT', '1. IT'),
                    ('CSE', '2. CSE'),
                    ('EEE', '3. EEE'),
                    ('AIDS', '4. AIDS'),
                    ('CIVIL', '5. CIVIL'),
                ],
                widget=forms.Select(attrs={
                    'class': 'info-box'
                })
            )