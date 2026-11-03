from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.dateparse import parse_time

from ..models import (
    Timetable,
    MyappStaff,
    Subject,
    Department,
    AcademicYear,
    YearSubject
)


def manage_timetable(request):

    # --------------------------------
    # 1. ADMIN LOGIN CHECK
    # --------------------------------

    admin_id = request.session.get('admin_id')

    if not admin_id:
        return redirect('admin_login')

    # --------------------------------
    # 2. GET DATABASE DATA
    # --------------------------------

    departments = Department.objects.all().order_by('dept_name')

    years = AcademicYear.objects.all().order_by('year_id')

    staff_list = MyappStaff.objects.all().order_by('name')

    subjects = YearSubject.objects.select_related(
        'subject',
        'department',
        'year'
    ).all()

    # --------------------------------
    # 3. HANDLE FORM SUBMISSION
    # --------------------------------

    if request.method == 'POST':

        action = request.POST.get('action')

        # --------------------------------
        # ADD TIMETABLE
        # --------------------------------

        if action == 'add':

            department_id = request.POST.get('department')
            year_id = request.POST.get('year')
            subject_id = request.POST.get('subject')
            staff_id = request.POST.get('staff')

            day = request.POST.get('day')

            start_time = parse_time(
                request.POST.get('start_time', '')
            )

            end_time = parse_time(
                request.POST.get('end_time', '')
            )

            room_number = request.POST.get(
                'room_number', ''
            ).strip()

            # Check required fields

            if not all([
                department_id,
                year_id,
                subject_id,
                staff_id,
                day,
                start_time,
                end_time
            ]):

                messages.error(
                    request,
                    'Please fill all required fields.'
                )

                return redirect('manage_timetable')

            # Check valid time

            if start_time >= end_time:

                messages.error(
                    request,
                    'End time must be later than start time.'
                )

                return redirect('manage_timetable')

            # Get selected records

            department = get_object_or_404(
                Department,
                id=department_id
            )

            year = get_object_or_404(
                AcademicYear,
                year_id=year_id
            )

            subject = get_object_or_404(
                Subject,
                id=subject_id
            )

            staff = get_object_or_404(
                MyappStaff,
                id=staff_id
            )

            # Check staff department

            if (staff.department or '').strip().lower() != department.dept_name.strip().lower():

                messages.error(
                    request,
                    'Selected staff does not belong to this department.'
                )

                return redirect('manage_timetable')

            # Check subject department and academic year

            valid_subject = YearSubject.objects.filter(
                subject=subject,
                department=department,
                year=year
            ).exists()

            if not valid_subject:

                messages.error(
                    request,
                    'This subject is not assigned to the selected department and year.'
                )

                return redirect('manage_timetable')

            # Check staff timetable overlap

            staff_overlap = Timetable.objects.filter(
                staff=staff,
                day=day,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exists()

            if staff_overlap:

                messages.error(
                    request,
                    'This staff member already has a class during this time.'
                )

                return redirect('manage_timetable')

            # Check classroom overlap

            if room_number:

                room_overlap = Timetable.objects.filter(
                    day=day,
                    room_number__iexact=room_number,
                    start_time__lt=end_time,
                    end_time__gt=start_time
                ).exists()

                if room_overlap:

                    messages.error(
                        request,
                        'This classroom is already occupied during this time.'
                    )

                    return redirect('manage_timetable')

            # Save timetable

            Timetable.objects.create(
                staff=staff,
                subject=subject,
                day=day,
                start_time=start_time,
                end_time=end_time,
                room_number=room_number,
                year=year
            )

            messages.success(
                request,
                'Timetable added successfully!'
            )

            return redirect('manage_timetable')

        # --------------------------------
        # DELETE TIMETABLE
        # --------------------------------

        elif action == 'delete':

            timetable_id = request.POST.get('timetable_id')

            timetable = get_object_or_404(
                Timetable,
                id=timetable_id
            )

            timetable.delete()

            messages.success(
                request,
                'Timetable deleted successfully!'
            )

            return redirect('manage_timetable')

    # --------------------------------
    # 4. DISPLAY TIMETABLE
    # --------------------------------

    timetable_list = Timetable.objects.select_related(
        'staff',
        'subject',
        'year'
    ).all().order_by(
        'day',
        'start_time'
    )

    # --------------------------------
    # 5. SEND DATA TO HTML
    # --------------------------------

    context = {
        'departments': departments,
        'years': years,
        'staff_list': staff_list,
        'subjects': subjects,
        'timetable_list': timetable_list,
    }

    return render(
        request,
        'admin/manage_timetable.html',
        context
    )