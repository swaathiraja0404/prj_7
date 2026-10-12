from django .views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ..models import MyappStaff, MyappStudent


def staff_dashboard(request):
    staff_id = request.session.get('staff_id')
    if not staff_id:
        return redirect('login')
    try:
        staff = MyappStaff.objects.get(id=staff_id)
    except MyappStaff.DoesNotExist:
        request.session.flush()
        return redirect('login')
    total_students = MyappStudent.objects.filter(department__iexact=staff.department ).count()
    return render(request,'students/staff_dashboard.html',{'staff': staff,'total_students': total_students})

