from django.shortcuts import render, redirect
from ..models import UserAuth, MyappStudent, MyappStaff, Department, Subject
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password


def admin_change_password(request):

    admin_id = request.session.get("admin_id")

    if not admin_id:
        return redirect("admin_login")

    admin = UserAuth.objects.filter(
        id=admin_id,
        role="Admin"
    ).first()

    if not admin:
        request.session.flush()
        return redirect("admin_login")

    if request.method == "POST":

        current_password = request.POST.get("current_password", "")
        new_password = request.POST.get("new_password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not check_password(current_password, admin.password or ""):
            messages.error(request, "Incorrect current password.")

        elif len(new_password) < 8:
            messages.error(request, "Password must contain at least 8 characters.")

        elif new_password != confirm_password:
            messages.error(request, "New passwords do not match.")

        else:
            admin.password = make_password(new_password)
            admin.save()

            messages.success(request, "Password changed successfully!")
            return redirect("admin_dashboard")

    return render(request, "admin/change_password.html", {
        "admin": admin
    })

def admin_dashboard(request):
    admin_id = request.session.get("admin_id")

    if not admin_id:
        return redirect("admin_login")

    admin = UserAuth.objects.filter(
        id=admin_id,
        role="Admin"
    ).first()

    if not admin:
        request.session.flush()
        return redirect("admin_login")

    context = {
        "admin": admin,
        "total_students": MyappStudent.objects.count(),
        "total_staff": MyappStaff.objects.count(),
        "total_departments": Department.objects.count(),
        "total_subjects": Subject.objects.count(),
    }

    return render(request, "admin/admin_dashboard.html", context)
    
def admin_logout(request):
    request.session.flush()
    return redirect("admin_login")
