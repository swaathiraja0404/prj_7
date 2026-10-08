from django .views import View
from django .shortcuts import render,redirect
from django.http import HttpResponse
from ..forms import Personal
from ..models import MyappStudent

def Student_personal_info(request):
    if request.method=="POST":
        form = Personal(request.POST,request.FILES)

        if form.is_valid():
            form.save()
            return redirect("Student_personal_info")
    else:
        form = Personal()
    return render(request,'students/personal.html',{'form':form})     
