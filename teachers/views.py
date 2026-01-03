from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TeacherCreateSerializer,AllTeacherInformationSerializer

from authentication.authenticate import TeacherJWTAuthentication
from authentication.permission import IsAdminTeacher
from .models import Teacher
from .pagination import TeacherListPagination



class TeacherCreateView(APIView):
    authentication_classes = [TeacherJWTAuthentication]
    permission_classes = [IsAdminTeacher]

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
    
class AllTeacherInformationView(APIView):
    authentication_classes = [TeacherJWTAuthentication]
    permission_classes = [IsAdminTeacher]
    def get(self, request):
        queryset = Teacher.objects.all().order_by("-id")

        paginator = TeacherListPagination()
        paginated_qs = paginator.paginate_queryset(queryset, request)
        serializer = AllTeacherInformationSerializer(paginated_qs, many=True)

        return paginator.get_paginated_response(serializer.data)
