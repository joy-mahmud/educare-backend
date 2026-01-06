from django.urls import path
from .views import StudentRegistrationApiView,AllStudentInfoView

urlpatterns = [
    path('registration/',StudentRegistrationApiView.as_view(), name='student-registration'),
    path('all-student-info/',AllStudentInfoView.as_view(),name='all-student-info')
]
