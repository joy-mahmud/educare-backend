from rest_framework import serializers
from django.db import transaction
from .models import AcademicClass, StudentResult, StudentSubject, ClassSubject
from students.models import Student
from django.db import transaction
class AcademicClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicClass
        fields = "__all__"

from rest_framework import serializers

class ClassSubjectSerializer(serializers.ModelSerializer):
    subject_id = serializers.IntegerField(source="subject.id")
    subject_name = serializers.CharField(source="subject.name")

    group_id = serializers.IntegerField(
        source="group.id",
        allow_null=True
    )

    group_name = serializers.CharField(
        source="group.name",
        allow_null=True
    )

    class Meta:
        model = ClassSubject
        fields = [
            "id",                # class_subject_id
            "subject_id",
            "subject_name",
            "subject_type",
            "group_id",
            "group_name",
        ]


class StudentMarkSerializer(serializers.Serializer):
    student = serializers.IntegerField()
    marks_obtained = serializers.DecimalField(max_digits=5, decimal_places=2)
    grade = serializers.CharField()


class BulkResultCreateSerializer(serializers.Serializer):
    exam = serializers.CharField()
    class_subject = serializers.IntegerField()
    results = StudentMarkSerializer(many=True)

    @transaction.atomic
    def create(self, validated_data):
        exam = validated_data["exam"]
        class_subject_id = validated_data["class_subject"]
        results_data = validated_data["results"]

        class_subject = ClassSubject.objects.get(id=class_subject_id)

        created_results = []

        for item in results_data:
            student_id = item["student"]
            marks = item["marks_obtained"]
            grade = item["grade"]
            student = Student.objects.get(id=student_id)

            # Get or create StudentSubject
            student_subject, _ = StudentSubject.objects.get_or_create(
                student=student,
                class_subject=class_subject
            )

            result = StudentResult.objects.create(
                student_subject=student_subject,
                exam=exam,
                marks_obtained=marks,
                grade=grade
            )

            created_results.append(result)

        return created_results