from django.urls import path
from .views import PaymentCreateView,StudentPaymentDetailsView,AdminPaymentListView, PaymentStatusUpdateView,StudentPaymentStatusView,PaymentSlipAPIView
urlpatterns = [
    path('create/',PaymentCreateView.as_view(),name='payment_create'),
    path('student-payment-details/',StudentPaymentDetailsView.as_view(),name='student-payment-details'),
    path('all-payments/',AdminPaymentListView.as_view(),name='all-payments'),
    path('update-status/<int:pk>', PaymentStatusUpdateView.as_view()),
    path("student-payment-status/", StudentPaymentStatusView.as_view(),name="student-payment-status"),
    path('payment-slip/',PaymentSlipAPIView.as_view(),name="payment-slip")

]
