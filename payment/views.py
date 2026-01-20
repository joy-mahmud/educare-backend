from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from students.models import Student
from .serializers import PaymentSerializer,StudentPaymentDetailsSerializer,AdminPaymentListSerializer,PaymentStatusUpdateSerializer
from authentication.authenticate import StudentJWTAuthentication , TeacherJWTAuthentication
from authentication.permission import IsStudentAuthenticated,IsAdminTeacher
from .models import Payment
from django.db.models import Case, When, Value, IntegerField
from .pagination import AdminPaymentListPagination
# Create your views here.

class PaymentCreateView(APIView):
    def post(self,request):
        phone_number = request.data.get("phoneNumber")
        
        student = Student.objects.filter(mobile = phone_number).first()        
        if not student:
            return Response({'message':"you are not registered with this number"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(student=student)
            return Response(
                {"message":"Payment Recorded successfully","transactionId":serializer.data["transactionId"]},
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,status=status.HTTP_400_BAD_REQUEST
        )
    
class StudentPaymentDetailsView(APIView):
    authentication_classes =[StudentJWTAuthentication]
    permission_classes =[IsStudentAuthenticated]
    
    def get(self,request):
        student = request.user
        payments = Payment.objects.filter(student= student).order_by('-createdAt')
        serializer = StudentPaymentDetailsSerializer(payments,many=True)

        return Response(serializer.data)
class StudentPaymentStatusView(APIView):
    def get(self, request):
        phone = request.GET.get("phone")

        payments = Payment.objects.filter(phoneNumber=phone, status="completed")

        paid_data = {
            "application": False,
            "admission": False,
            "registration": False,
            "exam_first": False,
            "exam_second": False,
            "tuition_months": []
        }

        for payment in payments:
            bd = payment.payment_breakdown

            if bd.get("application_fee", 0) > 0:
                paid_data["application"] = True

            if bd.get("admission_fee", 0) > 0:
                paid_data["admission"] = True

            if bd.get("registration_fee", 0) > 0:
                paid_data["registration"] = True

            exam = bd.get("exam_fee")
            if exam:
                if exam.get("first_semester", 0) > 0:
                    paid_data["exam_first"] = True
                if exam.get("second_semester", 0) > 0:
                    paid_data["exam_second"] = True

            tuition = bd.get("tuition_fee")
            if tuition:
                paid_data["tuition_months"].extend(tuition.get("months", []))

        paid_data["tuition_months"] = list(set(paid_data["tuition_months"]))

        return Response(paid_data)
class AdminPaymentListView(APIView):
    authentication_classes = [TeacherJWTAuthentication]
    permission_classes = [IsAdminTeacher]

    def get(self, request):
        payments = Payment.objects.annotate(
            pending_first=Case(
                When(status="pending", then=Value(0)),
                default=Value(1),
                output_field=IntegerField()
            )
        ).order_by("pending_first", "-createdAt")

        paginator = AdminPaymentListPagination()
        paginated_payments = paginator.paginate_queryset(payments, request)

        serializer = AdminPaymentListSerializer(paginated_payments, many=True)
        return paginator.get_paginated_response(serializer.data)
class PaymentStatusUpdateView(APIView):
    authentication_classes=[TeacherJWTAuthentication]
    permission_classes=[IsAdminTeacher]
    
    def patch(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)

        serializer = PaymentStatusUpdateSerializer(
            payment,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Payment status updated successfully",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)