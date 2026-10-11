from django .views import View
from django .shortcuts import render,redirect
from django.http import HttpResponse
from ..forms import Personal
from ..models import MyappStudent,UserAuth

def Student_personal_info(request):
    if request.method=="POST":
        form = Personal(request.POST,request.FILES)

        if form.is_valid():
            try:
                with transaction.atomic():
                    student = form.save()

                    UserAuth.objects.create(
                        user_id=student.id,
                        username=student.email,
                        password=make_password(
                            form.cleaned_data['password']
                        ),
                        role='Student'
                    )

                messages.success(
                    request,
                    "Student registered successfully!"
                )
                return redirect("Student_personal_info")

            except Exception as e:
                messages.error(request, f"Registration failed: {e}")

    else:
        form = Personal()

    return render(
        request,
        'students/personal.html',
        {'form': form}
    )