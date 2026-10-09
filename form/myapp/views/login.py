from django .views import View
from django .shortcuts import render,redirect
from django.http import HttpResponse
from ..forms import LoginForm
def log(request):
    if request.method=="POST":
        form = LoginForm(request.POST,request.FILES)

        if form.is_valid():
            form.save()
            return redirect("Student_personal_info")
    else:
        form = LoginForm()
    return render(request,'students/login.html',{'form':form})     
