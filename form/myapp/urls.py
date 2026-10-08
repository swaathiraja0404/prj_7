from  django.urls import path
from .views import Student_personal_info,staff_personal_info
urlpatterns=[
    path('info/',Student_personal_info,name="Student_personal_info"),
    path("staff/",staff_personal_info,name="staff_personal_info")

]