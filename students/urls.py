from django.urls import path
from .views import StudentRegistrationApiView

urlpatterns = [
    path('registration/',StudentRegistrationApiView.as_view(), name='student-registration')
]
