from django .views import View
from django .shortcuts import render,redirect
from django.http import HttpResponse
from ..forms import Personal
from ..models import MyappStudent

def Student_personal_info(request):
    form = Personal()
    return render(request,'students/personal.html',{'form':form})    