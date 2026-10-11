from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from ..forms import LoginForm
from ..models import UserAuth


def log(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']

            user = UserAuth.objects.filter(
                username=username,
                role=role
            ).first()

            if user and user.password and check_password(password, user.password):
                messages.success(request, "Login successful!")

                if role == 'Student':
                    return redirect("Student_personal_info")
                elif role == 'Staff':
                    return redirect("staff_personal_info")

            else:
                messages.error(request, "Invalid username or password.")

    else:
        form = LoginForm()

    return render(request, 'students/login.html', {'form': form})