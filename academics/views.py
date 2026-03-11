from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ClassSubject,StudentResult
from .serializers import ClassSubjectSerializer,BulkResultCreateSerializer,ResultViewSerializer,StudentExamResultSerializer
from django.db.models import Max, OuterRef, Subquery

class ClassSubjectAPIView(APIView):

    def get(self, request, class_id):

        subjects = ClassSubject.objects.filter(
            academic_class_id=class_id
        ).select_related(
            "subject",
            "group"
        )

        if not subjects.exists():
            return Response(
                {"message": "No subjects found for this class"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ClassSubjectSerializer(subjects, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class BulkResultCreateAPIView(APIView):

    def post(self, request):
        serializer = BulkResultCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Results created successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ViewResultAPIView(APIView):

    def post(self, request):

        class_id = request.data.get("class_id")
        class_subject_id = request.data.get("subject_id")
        exam = request.data.get("exam")
        classSubject = ClassSubject.objects.get(id=class_subject_id)
        subject_id = classSubject.subject_id

        if not class_id or not subject_id or not exam:
            return Response(
                {"error": "class_id, subject_id and exam are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        results = StudentResult.objects.filter(
            student_subject__class_subject__academic_class_id=class_id,
            student_subject__class_subject__subject_id=subject_id,
            exam=exam
        ).select_related(
            "student_subject__student",
            "student_subject__class_subject__subject",
            "student_subject__class_subject__academic_class"
        )

        serializer = ResultViewSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StudentExamResultAPIView(APIView):

    def post(self, request):

        student_id = request.data.get("student_id")
        exam = request.data.get("exam")

        if not student_id or not exam:
            return Response(
                {"error": "student_id and exam are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Subquery to get highest marks per subject
        highest_marks_subquery = StudentResult.objects.filter(
            student_subject__class_subject__subject=OuterRef(
                "student_subject__class_subject__subject"
            ),
            exam=exam
        ).values(
            "student_subject__class_subject__subject"
        ).annotate(
            highest=Max("marks_obtained")
        ).values("highest")[:1]

        results = StudentResult.objects.filter(
            student_subject__student_id=student_id,
            exam=exam
        ).select_related(
            "student_subject__class_subject__subject"
        ).annotate(
            highest_marks=Subquery(highest_marks_subquery)
        )

        serializer = StudentExamResultSerializer(results, many=True)

        return Response(serializer.data)