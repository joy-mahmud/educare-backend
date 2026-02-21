from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ClassSubject
from .serializers import ClassSubjectSerializer


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
