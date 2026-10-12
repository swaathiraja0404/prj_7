from django .views import View
from django .shortcuts import render,redirect
from django.http import HttpResponse
from ..forms import StaffPersonal
from ..models import MyappStaff,UserAuth
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.hashers import make_password


def staff_personal_info(request):
    if request.method == "POST":
        form = StaffPersonal(request.POST, request.FILES)

        if form.is_valid():
            username = form.cleaned_data['email']
            raw_password = form.cleaned_data['phone']

            try:
                with transaction.atomic():

                 
                    staff = form.save()
                    
                    UserAuth.objects.create(
                        user_id=staff.id,
                        username=staff.email,
                        password=make_password(staff.phone),
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


