from django.urls import path
from .views import ClassSubjectAPIView,BulkResultCreateAPIView

urlpatterns = [
    path("class-subjects/<int:class_id>/",ClassSubjectAPIView.as_view(),name="class-subjects",),
    path("bulk-result-create/",BulkResultCreateAPIView.as_view(),name="bulk-result-create",),
]
