from django .views import View
from django .shortcuts import render,redirect
from django.http import HttpResponse
from ..forms import StaffPersonal
from ..models import MyappStaff,UserAuth,Timetable,YearSubject,AcademicYear
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.hashers import make_password


def staff_personal_info(request):
    if request.method == "POST":
        form = StaffPersonal(request.POST, request.FILES)

        if form.is_valid():
            try:
                with transaction.atomic():
                    staff = form.save()

                    UserAuth.objects.create(
                        user_id=staff.id,
                        username=staff.email,
                        password=make_password(staff.phone),
                        role='Staff'
                    )

                    # Get subjects for this staff's department
                    department_subjects = YearSubject.objects.filter(
                        department__dept_name__iexact=staff.department
                    ).select_related('subject', 'year').order_by(
                        'year_id', 'subject__subject_code'
                    )

                    # College timetable periods
                    periods = [
                        (time(9, 0), time(10, 0)),
                        (time(10, 0), time(11, 0)),
                        # 11:00–11:15 AM break
                        (time(11, 15), time(12, 15)),
                        (time(12, 15), time(13, 15)),
                        # 1:15–2:15 PM lunch
                        (time(14, 15), time(15, 15)),
                        (time(15, 15), time(16, 15)),
                    ]

                    days = [
                        'Monday',
                        'Tuesday',
                        'Wednesday',
                        'Thursday',
                        'Friday',
                    ]

                    # Create timetable for each academic year
                    for academic_year in AcademicYear.objects.all():
                        subjects = list(
                            department_subjects.filter(
                                year=academic_year
                            ).values_list(
                                'subject_id', flat=True
                            ).distinct()
                        )

                        if not subjects:
                            continue

                        for day_index, day in enumerate(days):
                            for period_index, (start, end) in enumerate(periods):
                                subject_id = subjects[
                                    (day_index * len(periods) + period_index)
                                    % len(subjects)
                                ]

                                # Do not create duplicate day/time entries
                                exists = Timetable.objects.filter(
                                    staff=staff,
                                    year=academic_year,
                                    day=day,
                                    start_time=start
                                ).exists()

                                if not exists:
                                    Timetable.objects.create(
                                        staff=staff,
                                        subject_id=subject_id,
                                        year=academic_year,
                                        day=day,
                                        start_time=start,
                                        end_time=end,
                                        room_number='Room 201'
                                    )

                messages.success(
                    request,
                    "Staff information and timetable saved successfully!"
                )
                return redirect("staff_personal_info")

            except Exception as e:
                messages.error(
                    request,
                    f"Unable to save staff information: {e}"
                )

    else:
        form = StaffPersonal()

    return render(
        request,
        'students/staff_personal.html',
        {'form': form}
    )

