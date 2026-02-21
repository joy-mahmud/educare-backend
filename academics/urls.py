from django.urls import path
from .views import ClassSubjectAPIView

urlpatterns = [
    path("class-subjects/<int:class_id>/",ClassSubjectAPIView.as_view(),name="class-subjects",),
]
