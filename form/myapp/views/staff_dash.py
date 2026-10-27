from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from ..forms import StudentMarkForm,YearSubjectForm
from ..models import MyappStaff, MyappStudent, Subject, Timetable, StudentMark, UserAuth,YearSubject, AcademicYear
from django.db.models import Case, When, Value, IntegerField


from datetime import time
def staff_dashboard(request):
    staff_id = request.session.get('staff_id')

    if not staff_id:
        return redirect('login')

    try:
        staff = MyappStaff.objects.get(id=staff_id)
    except MyappStaff.DoesNotExist:
        request.session.flush()
        return redirect('login')

    department = (staff.department or '').strip().upper()

    # --------------------------------
    # 1. Students - logged-in staff department only
    # --------------------------------
    students = MyappStudent.objects.filter(
        department__iexact=department
    )

    selected_year = request.GET.get('year', '').strip()

    if selected_year.isdigit():
        students = students.filter(year_id=int(selected_year))

    students = students.order_by('id')
    total_students = students.count()

    # --------------------------------
    # 2. Subjects - staff department only
    # --------------------------------
    year_subjects = YearSubject.objects.filter(
        department__dept_name__iexact=department
    )

    if selected_year.isdigit():
        year_subjects = year_subjects.filter(
            year_id=int(selected_year)
        )

    subjects = Subject.objects.filter(
        id__in=year_subjects.values_list(
            'subject_id',
            flat=True
        )
    ).order_by('subject_code')

    # --------------------------------
    # 3. Timetable - logged-in staff only
    # --------------------------------
    timetable_query = Timetable.objects.filter(
        staff_id=staff.id,
        staff__department__iexact=department,
        day__in=[
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday'
        ]
    ).select_related(
        'staff',
        'subject',
        'year'
    )

    # Filter by selected year when provided
    if selected_year.isdigit():
        timetable_query = timetable_query.filter(
            year_id=int(selected_year)
        )

    timetable_records = list(
        timetable_query.order_by(
            'day',
            'start_time'
        )
    )

    # --------------------------------
    # 4. Weekly timetable configuration
    # --------------------------------
    days = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday'
    ]

    periods = [
        ('09:00', '9–10 AM'),
        ('10:00', '10–11 AM'),
        ('BREAK', '11–11:15 AM'),
        ('11:15', '11:15–12:15 PM'),
        ('12:15', '12:15–1:15 PM'),
        ('LUNCH', '1:15–2:15 PM'),
        ('14:15', '2:15–3:15 PM'),
        ('15:15', '3:15–4:15 PM'),
    ]

    # --------------------------------
    # 5. Build timetable rows
    # --------------------------------
    timetable_rows = []

    for period_key, period_label in periods:

        if period_key in ['BREAK', 'LUNCH']:
            timetable_rows.append({
                'label': period_label,
                'kind': period_key.lower(),
                'cells': [
                    {
                        'subject': period_key,
                        'code': ''
                    }
                    for day in days
                ]
            })
            continue

        cells = []

        for day in days:
            record = next(
                (
                    item
                    for item in timetable_records
                    if item.day.strip().lower() == day.lower()
                    and item.start_time.strftime('%H:%M') == period_key
                ),
                None
            )

            if record:
                cells.append({
                    'subject': record.subject.subject_name,
                    'code': record.subject.subject_code
                })
            else:
                cells.append({
                    'subject': '—',
                    'code': ''
                })

        timetable_rows.append({
            'label': period_label,
            'kind': 'normal',
            'cells': cells
        })

    # --------------------------------
    # 6. Academic years
    # --------------------------------
    years = AcademicYear.objects.all().order_by('year_id')

    context = {
        'staff': staff,
        'students': students,
        'total_students': total_students,
        'subjects': subjects,
        'timetable': timetable_records,
        'timetable_rows': timetable_rows,
        'days': days,
        'years': years,
        'selected_year': selected_year,
    }

    return render(
        request,
        'students/staff_dashboard.html',
        context
    )
def add_student_marks(request, student_id):
    staff_id = request.session.get('staff_id')
    if not staff_id:
        return redirect('login')
    staff = get_object_or_404(MyappStaff, id=staff_id)
    staff_department = (staff.department or '').strip().upper()
    student = get_object_or_404(
        MyappStudent,
        id=student_id,
        department__iexact=staff_department
    )
    department_codes = {
        'IT': 'IT',
        'CSE': 'CSE',
        'EEE': 'EEE',
        'AIDS': 'AIDS',
        'CIVIL': 'CIV'
    }

    prefix = department_codes.get(staff_department)

    if prefix:
        subjects = Subject.objects.filter(
            subject_code__startswith=prefix
        ).order_by('subject_code')
    else:
        subjects = Subject.objects.none()
    if request.method == 'POST':

        form = StudentMarkForm(
            request.POST,
            subjects=subjects
        )

        if form.is_valid():

            subject = form.cleaned_data['subject']
            internal = form.cleaned_data['internal_marks']
            external = form.cleaned_data['external_marks']

            mark, created = StudentMark.objects.update_or_create(
                student=student,
                subject=subject,
                defaults={
                    'staff': staff,
                    'internal_marks': internal,
                    'external_marks': external
                }
            )

            if created:
                messages.success(
                    request,
                    'Marks added successfully!'
                )
            else:
                messages.success(
                    request,
                    'Marks updated successfully!'
                )

            return redirect(
                'add_student_marks',
                student_id=student.id
            )
    else:
        form = StudentMarkForm(subjects=subjects)
    saved_marks = StudentMark.objects.filter(
        student=student
    ).select_related(
        'subject'
    ).order_by(
        'subject__subject_code'
    )

    return render(
        request,
        'students/add_student_marks.html',
        {
            'staff': staff,
            'student': student,
            'form': form,
            'saved_marks': saved_marks
        }
    )

def staff_logout(request):
    request.session.flush()
    return redirect('log')
    
def staff_change_password(request):
    staff_id = request.session.get('staff_id')

    if not staff_id:
        return redirect('log')

    staff = get_object_or_404(MyappStaff, id=staff_id)

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = UserAuth.objects.filter(
            user_id=staff.id,
            role='Staff'
        ).first()

        if not user:
            messages.error(request, 'Staff login account not found.')

        elif not user.password or not check_password(
            old_password, user.password
        ):
            messages.error(request, 'Old password is incorrect.')

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

        else:
            user.password = make_password(new_password)
            user.save(update_fields=['password'])

            messages.success(
                request,
                'Password changed successfully!'
            )

            return redirect('staff_dashboard')

    return render(
        request,
        'students/staff_change_password.html',
        {'staff': staff}
    )

def year_subject_view(request):
    staff_id = request.session.get('staff_id')

    if not staff_id:
        return redirect('login')

    staff = get_object_or_404(MyappStaff, id=staff_id)

    if request.method == 'POST':
        form = YearSubjectForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Department, year and subject mapped successfully!'
            )

            return redirect('year_subject')
    else:
        form = YearSubjectForm()

    mappings = YearSubject.objects.select_related(
        'department', 'year', 'subject'
    ).all()

    return render(
        request,
        'students/year_subject.html',
        {
            'staff': staff,
            'form': form,
            'mappings': mappings,
        }
    )