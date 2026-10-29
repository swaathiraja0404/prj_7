from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from ..models import MyappStudent, StudentMark, YearSubject, Timetable,UserAuth
from django.contrib.auth.hashers import make_password, check_password

def student_dashboard(request):
    student_id = request.session.get('student_id')

    if not student_id:
        messages.error(request, "Please login first.")
        return redirect('log')

    student = get_object_or_404(MyappStudent, id=student_id)

    marks = StudentMark.objects.filter(
        student=student
    ).select_related('subject', 'staff')

    subjects = YearSubject.objects.filter(
        department__dept_name__iexact=student.department,
        year=student.year
    ).select_related('subject', 'year')

    # Get timetable for the student's department and academic year
    timetable = Timetable.objects.filter(
        staff__department__iexact=student.department,
        year=student.year
    ).select_related(
        'staff', 'subject', 'year'
    ).order_by('start_time', 'day')

    # Weekday columns
    days = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
    ]

    # Create unique time slots
    time_slots = []

    for item in timetable:
        slot = (item.start_time, item.end_time)

        if slot not in time_slots:
            time_slots.append(slot)

    time_slots.sort(key=lambda slot: slot[0])

    # Build the weekly timetable grid
    timetable_rows = []

    for start_time, end_time in time_slots:
        cells = []

        for day in days:
            matching_class = timetable.filter(
                day=day,
                start_time=start_time,
                end_time=end_time
            ).first()

            if matching_class:
                cells.append({
                    'code': matching_class.subject.subject_code,
                    'subject': matching_class.subject.subject_name,
                    'staff': matching_class.staff.name,
                    'room': matching_class.room_number,
                })
            else:
                cells.append({
                    'code': '',
                    'subject': '',
                    'staff': '',
                    'room': '',
                })

        timetable_rows.append({
            'label': (
                f"{start_time.strftime('%I:%M %p')} - "
                f"{end_time.strftime('%I:%M %p')}"
            ),
            'cells': cells,
        })

    context = {
        'student': student,
        'marks': marks,
        'subjects': subjects,
        'timetable': timetable,
        'days': days,
        'timetable_rows': timetable_rows,
    }

    return render(
        request,
        'students/student_dashboard.html',
        context
    )


def student_change_password(request):
    student_id = request.session.get('student_id')

    if not student_id:
        messages.error(request, "Please login first.")
        return redirect('log')

    student = get_object_or_404(
        MyappStudent,
        id=student_id
    )

    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        user = UserAuth.objects.filter(
            user_id=student.id,
            role__iexact='Student'
        ).first()

        if not user:
            messages.error(
                request,
                'Student login account not found.'
            )

        elif not user.password or not check_password(
            old_password, user.password
        ):
            messages.error(
                request,
                'Old password is incorrect.'
            )

        elif len(new_password) < 8:
            messages.error(
                request,
                'New password must contain at least 8 characters.'
            )

        elif new_password != confirm_password:
            messages.error(
                request,
                'New password and confirm password do not match.'
            )

        elif old_password == new_password:
            messages.error(
                request,
                'New password must be different from the old password.'
            )

        else:
            user.password = make_password(new_password)
            user.save(update_fields=['password'])

            messages.success(
                request,
                'Password changed successfully!'
            )

            return redirect('student_dashboard')

    return render(
        request,
        'students/change_password.html',
        {'student': student}
    )

