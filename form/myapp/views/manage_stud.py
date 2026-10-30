from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import MyappStudent, UserAuth, AcademicYear

def manage_students(request):

    admin_id = request.session.get("admin_id")

    if not admin_id:
        return redirect("admin_login")

    students = MyappStudent.objects.all().order_by("id")

    departments = (
        MyappStudent.objects
        .exclude(department__isnull=True)
        .exclude(department__exact="")
        .values_list("department", flat=True)
        .distinct()
        .order_by("department")
    )

    years = AcademicYear.objects.all().order_by("year_id")

    return render(request, "admin/manage_students.html", {
        "students": students,
        "departments": departments,
        "years": years
    })

def delete_student(request, student_id):

    admin_id = request.session.get("admin_id")

    if not admin_id:
        return redirect("admin_login")

    student = get_object_or_404(MyappStudent, id=student_id)

    if request.method == "POST":

        UserAuth.objects.filter(
            user_id=student.id,
            role="Student"
        ).delete()

        student.delete()

        messages.success(request, "Student deleted successfully!")

    return redirect("manage_students")