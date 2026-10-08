from django .views import View
from django .shortcuts import render,redirect
from django.http import HttpResponse
from ..forms import StaffPersonal
from ..models import MyappStaff

def staff_personal_info(request):
    if request.method=="POST":
        form = StaffPersonal(request.POST,request.FILES)

        if form.is_valid():
            form.save()
            return redirect("staff_personal_info")
    else:
        form = StaffPersonal()
    return render(request,'students/staff_personal.html',{'form':form})     
