from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TeacherCreateSerializer

# from authentication.authenticate import TeacherJWTAuthentication
# from authentication.permission import IsAdminTeacher
from .models import Teacher



class TeacherCreateView(APIView):
    # authentication_classes = [TeacherJWTAuthentication]
    # permission_classes = [IsAdminTeacher]

    def post(self, request):
        serializer = TeacherCreateSerializer(data=request.data)

        if serializer.is_valid():
            teacher = serializer.save()
            return Response(
                {
                    "message": "Teacher created successfully",
                    "data": {
                        "teacherId": teacher.teacherId,
                    }
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
