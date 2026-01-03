from django.urls import path
from .views import TeacherCreateView,AllTeacherInformationView
urlpatterns=[
    path('create-teacher/',TeacherCreateView.as_view(), name='create-teacher'),
    path('all-teachers-info/',AllTeacherInformationView.as_view(),name='all-teacher-info')
]