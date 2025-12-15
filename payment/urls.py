from django.urls import path
from .views import PaymentCreateView,StudentPaymentDetailsView
urlpatterns = [
    path('create/',PaymentCreateView.as_view(),name='payment_create'),
    path('student-payment-details/',StudentPaymentDetailsView.as_view(),name='student-payment-details')
]
