from django import forms
from .models import MyappStudent,MyappStaff,Department,UserAuth
class Personal(forms.ModelForm):
        class Meta:
            model=MyappStudent
            fields = ['name','age','dod','phone','email']
        
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
        
        dod = forms.DateField(    widget=forms.TextInput(attrs=
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
                fields = ['name','age','dod','phone','email','department']
        
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
            
            dod = forms.DateField(    widget=forms.TextInput(attrs=
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
            
            department = forms.ModelChoiceField(
                queryset=Department.objects.all(),
                empty_label="Select Department",
                widget=forms.Select(attrs={
                    "class": "info-box"
                })
            )

class LoginForm(forms.Form):
            class Meta:
                    model=MyappStaff
                    fields = ['username','role']

            ROLE_CHOICES = [
                ('', 'Select Role'),
                ('Student', 'Student'),
                ('Staff', 'Staff'),
            ]

            role = forms.ChoiceField(
                choices=ROLE_CHOICES,
                widget=forms.Select(attrs={
                    'class': 'info-box'
                })
            )
            user_id = forms.IntegerField(
                widget=forms.NumberInput(attrs={
                    'class': 'info-box', 
                    'placeholder': 'Enter your User ID' 
                }) 
            )
            username = forms.CharField(
                max_length=254,
                widget=forms.TextInput(attrs={
                    'class': 'info-box',
                    'placeholder': 'Enter your username or email'
                })
            )

            password = forms.CharField(
                widget=forms.PasswordInput(attrs={
                    'class': 'info-box',
                    'placeholder': 'Enter your password'
                })
            )

