from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from students.models import Student
from .serializers import PaymentSerializer,StudentPaymentDetailsSerializer
from authentication.authenticate import StudentJWTAuthentication
from authentication.permission import IsStudentAuthenticated
from .models import Payment
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