from  django.urls import path
from .views import Student_personal_info,staff_personal_info,log,staff_dashboard
urlpatterns=[
    path('info/',Student_personal_info,name="Student_personal_info"),
    path("staff/",staff_personal_info,name="staff_personal_info"),
    path("log/",log,name="log"),
    path("sd/",staff_dashboard,name="staff_dashboard")

]