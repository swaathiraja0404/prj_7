
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from ..forms import LoginForm
from ..models import UserAuth,MyappStaff
def log(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            user = UserAuth.objects.filter(
                username=username,
                role=role).first()

            if user and user.password and check_password(password, user.password):

                if role == 'Student':
                    messages.success(request, "Login successful!")
                    return render("student_dashboard.html")

                elif role == 'Staff':

                    if not user.user_id:
                        messages.error(
                            request,
                            "Your staff account is not linked to a staff record."
                        )
                        return redirect('login')

                    request.session['staff_id'] = user.user_id

                    messages.success(request, "Login successful!")
                    return redirect("staff_dashboard")

            else:
                messages.error(request, "Invalid username or password.")

    else:
        form = LoginForm()

    return render(request, 'students/login.html', {'form': form})

