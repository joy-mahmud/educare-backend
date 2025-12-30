from django.urls import path
from .views import TeacherCreateView
urlpatterns=[
    path('create-teacher/',TeacherCreateView.as_view(), name='create-teacher'),
]