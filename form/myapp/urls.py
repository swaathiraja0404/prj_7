from  django.urls import path
from .views import Student_personal_info, staff_personal_info, log, staff_dashboard, add_student_marks,staff_change_password,staff_logout,year_subject_view
urlpatterns=[
    path('info/',Student_personal_info,name="Student_personal_info"),
    path("staff/",staff_personal_info,name="staff_personal_info"),
    path("log/",log,name="log"),
    path("sd/",staff_dashboard,name="staff_dashboard"),
    path('student/<int:student_id>/marks/', add_student_marks, name='add_student_marks'),
    path('staff-logout/', staff_logout,name='staff_logout'),
    path('staff/change-password/',  staff_change_password,name='staff_change_password'),
    path('year-subject/',year_subject_view, name='year_subject'),
]