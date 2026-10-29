from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import UserAuth


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = UserAuth.objects.filter(
            username=username,
            role="Admin"
        ).first()

        if user and user.password and check_password(password, user.password):
            request.session["admin_id"] = user.id
            messages.success(request, "Admin login successful!")
            return redirect("admin_dashboard")

        messages.error(request, "Invalid admin username or password.")

    return render(request, "admin/admin_login.html")


