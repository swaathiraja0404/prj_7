from  django.urls import path
from .views import Student_personal_info
urlpatterns=[
    path('info/',Student_personal_info,name="Student_personal_info")
]