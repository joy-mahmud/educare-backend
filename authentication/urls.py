from django.urls import path
from .views import SetPasswordView,StudentLoginView,TeacherRegistrationView,TeacherLoginView
urlpatterns = [
    path('set-password/',SetPasswordView.as_view(), name='set-password'),
    path('student-login/',StudentLoginView.as_view(),name="student-login"),
    path('teacher-registration/',TeacherRegistrationView.as_view(),name="teacher-registration"),
    path('teacher-login/',TeacherLoginView.as_view(),name="teacher-login")

]