from django .views import View
from django .shortcuts import render,redirect
from django.http import HttpResponse
from ..forms import Personal
from ..models import MyappStudent,UserAuth
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.hashers import make_password

def Student_personal_info(request):
    if request.method=="POST":
        form = Personal(request.POST,request.FILES)
        if form.is_valid():
            username = form.cleaned_data['email']
            raw_password = form.cleaned_data['phone']
            try:
                with transaction.atomic():
                    student = form.save()
                    UserAuth.objects.create(
                        user_id=student.id,
                        username=student.email,
                        password=make_password(student.phone),
                        role='Student'
                    )

                messages.success(
                    request,
                    "Student registered successfully!"
                )
                return redirect("Student_personal_info")

            except Exception:
                messages.error(
                    request,
                    "Unable to save the information. Check whether this username already exists."
                )
    else:
        form = Personal()

    return render(
        request,
        'students/personal.html',
        {'form': form}
    )