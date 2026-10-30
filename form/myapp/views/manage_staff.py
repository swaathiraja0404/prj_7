from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import MyappStaff, UserAuth
def manage_staff(request):
    admin_id = request.session.get("admin_id")

    if not admin_id:
        return redirect("admin_login")

    staff_list = MyappStaff.objects.all().order_by("id")

    return render(
        request,
        "admin/manage_staff.html",
        {"staff_list": staff_list}
    )


def delete_staff(request, staff_id):
    admin_id = request.session.get("admin_id")

    if not admin_id:
        return redirect("admin_login")

    staff = get_object_or_404(MyappStaff, id=staff_id)

    if request.method == "POST":
        # Delete staff login account
        UserAuth.objects.filter(user_id=staff.id, role="Staff").delete()

        # Delete staff record
        staff.delete()

        messages.success(request, "Staff deleted successfully!")

    return redirect("manage_staff")
