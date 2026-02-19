from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentSerializer,AllStudentInfoSerializer,StudentsAccordingClassSerializer
from .models import Student 
from .pagination import StudentPagination
class StudentRegistrationApiView(APIView):
    def post(self,request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Student created successfully"},status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class AllStudentInfoView(APIView):
    def get(self, request):
        queryset = Student.objects.order_by("-createdAt")

        paginator = StudentPagination()
        page = paginator.paginate_queryset(queryset, request)

        serializer = AllStudentInfoSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data) 

class StudentsByClassAPIView(APIView):
    def get(self, request, class_id):

        students = Student.objects.select_related("studentClass").filter(studentClass_id=class_id)

        serializer = StudentsAccordingClassSerializer(students, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
