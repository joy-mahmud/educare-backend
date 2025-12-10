from django.urls import path
from .views import SetPasswordView,StudentLoginView
urlpatterns = [
    path('set-password/',SetPasswordView.as_view(), name='set-password'),
    path('student-login/',StudentLoginView.as_view(),name="student-login")

]