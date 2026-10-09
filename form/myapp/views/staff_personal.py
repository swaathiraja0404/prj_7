from django .views import View
from django .shortcuts import render,redirect
from django.http import HttpResponse
from ..forms import StaffPersonal
from ..models import MyappStaff
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.hashers import make_password


def staff_personal_info(request):
    if request.method == "POST":
        form = StaffPersonal(request.POST, request.FILES)

        if form.is_valid():
            username = form.cleaned_data['email']
            raw_password = form.cleaned_data['password']

            try:
                with transaction.atomic():

                 
                    form.save()

                    
                    UserAuth.objects.create(
                        username=username,
                        password=make_password(raw_password),
                        role='Staff'
                    )

                messages.success(
                    request,
                    "Staff information saved successfully!"
                )
                return redirect("staff_personal_info")

            except Exception:
                messages.error(
                    request,
                    "Unable to save the information. Check whether this username already exists."
                )

    else:
        form = StaffPersonal()
    return render(request,'students/staff_personal.html',{'form':form})     


