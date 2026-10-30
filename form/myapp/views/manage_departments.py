from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import ProtectedError
from ..models import Department, YearSubject

def manage_departments(request):

    admin_id = request.session.get("admin_id")

    if not admin_id:
        return redirect("admin_login")

    if request.method == "POST":

        dept_name = request.POST.get("dept_name", "").strip()

        if not dept_name:
            messages.error(request, "Department name is required.")

        elif Department.objects.filter(dept_name__iexact=dept_name).exists():
            messages.error(request, "Department already exists.")

        else:
            Department.objects.create(dept_name=dept_name)
            messages.success(request, "Department added successfully!")

        return redirect("manage_departments")

    departments = Department.objects.all().order_by("id")

    department_data = []

    for dept in departments:
        subject_count = YearSubject.objects.filter(
            department=dept
        ).count()

        department_data.append({
            "department": dept,
            "subject_count": subject_count
        })

    return render(
        request,
        "admin/manage_departments.html",
        {"department_data": department_data}
    )


def edit_department(request, department_id):

    admin_id = request.session.get("admin_id")

    if not admin_id:
        return redirect("admin_login")

    department = get_object_or_404(Department, id=department_id)

    if request.method == "POST":

        dept_name = request.POST.get("dept_name", "").strip()

        if not dept_name:
            messages.error(request, "Department name is required.")

        elif Department.objects.filter(
            dept_name__iexact=dept_name
        ).exclude(id=department_id).exists():

            messages.error(request, "Department already exists.")

        else:
            department.dept_name = dept_name
            department.save()

            messages.success(request, "Department updated successfully!")

        return redirect("manage_departments")

    return redirect("manage_departments")


def delete_department(request, department_id):

    admin_id = request.session.get("admin_id")

    if not admin_id:
        return redirect("admin_login")

    department = get_object_or_404(Department, id=department_id)

    if request.method == "POST":

        if YearSubject.objects.filter(department=department).exists():

            messages.error(
                request,
                "Cannot delete this department. Subjects are assigned to it."
            )

        else:
            department.delete()

            messages.success(
                request,
                "Department deleted successfully!"
            )

    return redirect("manage_departments")