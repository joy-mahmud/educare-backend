from django.urls import path
from .views import ClassSubjectAPIView,BulkResultCreateAPIView,ViewResultAPIView,StudentExamResultAPIView,ExamRoutineListAPIView,GenerateAllStudentAdmitCard

urlpatterns = [
    path("class-subjects/<int:class_id>/",ClassSubjectAPIView.as_view(),name="class-subjects",),
    path("bulk-result-create/",BulkResultCreateAPIView.as_view(),name="bulk-result-create",),
    path("view-results/", ViewResultAPIView.as_view(), name="view-results"),
    path("student-exam-marks/",StudentExamResultAPIView.as_view(),name="sutdent-exam-marks"),
    path("exam-routine/",ExamRoutineListAPIView.as_view(),name="get-exam-routine"),
    path("all-student-admit-card/",GenerateAllStudentAdmitCard.as_view(),name="generate-all-student-admit-card")
]
