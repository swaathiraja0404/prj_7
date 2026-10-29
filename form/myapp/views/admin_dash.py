from django.shortcuts import render, redirect
from ..models import UserAuth, MyappStudent, MyappStaff, Department, Subject


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
    request.session.pop("admin_id", None)
    return redirect("admin_login")
