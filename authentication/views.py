from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import jwt
from datetime import datetime, timedelta,timezone
from django.conf import settings

from .serializers import SetPasswordSerializer,StudentLoginSerializer,TeacherLoginSerializer,TeacherRegistrationSerializer

class SetPasswordView(APIView):
    def post(self,request):
        serializer = SetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Password set successfully"},status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class StudentLoginView(APIView):
    def post(self, request):
        serializer = StudentLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"message": "Invalid credentials", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        auth = serializer.validated_data['auth']
        student = auth.student  # your custom logic
        payload = {
            "user_type": "student",
            "student_id": student.id,
            "role":"student",
            "phone": auth.phone,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(days=7),
        }
        access_token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")
        # Create JWT tokens

        return Response({
            "message": "Login successful",
            "student": {
                "id": student.id,
                "name": student.studentName,
                "mobile": student.mobile,
                # add any fields you want
            },
            "token": access_token
        }, status=status.HTTP_200_OK)

class TeacherRegistrationView(APIView):
    def post(self, request):
        serializer = TeacherRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        auth = serializer.save()

        return Response({
            "message": "Registration successful",
            "teacher": {
                "teacherId": auth.teacher.teacherId,
                "name": auth.teacher.name,
                "email": auth.email,
                "phone": auth.teacher.phone,
                "dateOfBirth": auth.teacher.dateOfBirth
            },
            "createdAt": auth.createdAt
        }, status=status.HTTP_201_CREATED)

class TeacherLoginView(APIView):
    def post(self, request):
        serializer = TeacherLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth = serializer.validated_data["auth"]
        teacher = auth.teacher

        payload = {
            "user_type": "teacher",
            "teacher_id": teacher.id,
            "role": teacher.role,
            "exp": datetime.now(timezone.utc) + timedelta(days=7),
            "iat": datetime.now(timezone.utc),
        }

        token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")

        return Response({
            "message": "Login successful",
            "teacher": {
                "teacherId": teacher.teacherId,
                "name": teacher.name,
                "email": auth.email,
            },
            "token": token
        }, status=status.HTTP_200_OK)



