from django.urls import path
from .views import StudentRegistrationApiView,AllStudentInfoView,StudentsByClassAPIView

urlpatterns = [
    path('registration/',StudentRegistrationApiView.as_view(), name='student-registration'),
    path('all-student-info/',AllStudentInfoView.as_view(),name='all-student-info'),
    path("student-by-class/<int:class_id>/", StudentsByClassAPIView.as_view(),name="students-by-class"
    ),
]
