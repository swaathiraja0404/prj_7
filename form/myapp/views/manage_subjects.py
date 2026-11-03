from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from ..models import Subject, Department, AcademicYear, YearSubject


def manage_subjects(request):

    # Check Admin Login
    admin_id = request.session.get('admin_id')

    if not admin_id:
        return redirect('admin_login')

    # Get Departments and Academic Years
    departments = Department.objects.all()
    years = AcademicYear.objects.all()

    # Handle POST Request
    if request.method == 'POST':

        action = request.POST.get('action')

        # --------------------------------
        # ADD SUBJECT
        # --------------------------------
        if action == 'add':

            subject_code = request.POST.get('subject_code', '').strip()
            subject_name = request.POST.get('subject_name', '').strip()
            department_id = request.POST.get('department')
            year_id = request.POST.get('year')

            if not subject_code or not subject_name or not department_id or not year_id:

                messages.error(request, 'Please fill all the fields.')

            else:

                department = get_object_or_404(
                    Department,
                    id=department_id
                )

                year = get_object_or_404(
                    AcademicYear,
                    year_id=year_id
                )

                subject = Subject.objects.filter(
                    subject_code=subject_code
                ).first()

                if subject:

                    if subject.subject_name != subject_name:

                        messages.error(
                            request,
                            'This subject code already exists with a different subject name.'
                        )

                        return redirect('manage_subjects')

                else:

                    subject = Subject.objects.create(
                        subject_code=subject_code,
                        subject_name=subject_name
                    )

                # Assign Subject to Department and Year
                assignment, created = YearSubject.objects.get_or_create(
                    subject=subject,
                    department=department,
                    year=year
                )

                if created:

                    messages.success(
                        request,
                        'Subject added successfully!'
                    )

                else:

                    messages.warning(
                        request,
                        'This subject is already assigned to this department and year.'
                    )

            return redirect('manage_subjects')

        # --------------------------------
        # DELETE SUBJECT ASSIGNMENT
        # --------------------------------
        elif action == 'delete':

            assignment_id = request.POST.get('assignment_id')

            assignment = get_object_or_404(
                YearSubject,
                id=assignment_id
            )

            assignment.delete()

            messages.success(
                request,
                'Subject assignment deleted successfully!'
            )

            return redirect('manage_subjects')

    # --------------------------------
    # DISPLAY SUBJECTS
    # --------------------------------
    subjects = YearSubject.objects.select_related(
        'subject',
        'department',
        'year'
    ).all().order_by(
        'department__dept_name',
        'year__year_id',
        'subject__subject_code'
    )

    # Send Data to HTML
    context = {
        'departments': departments,
        'years': years,
        'subjects': subjects,
    }

    return render(
        request,
        'admin/manage_subjects.html',
        context
    )