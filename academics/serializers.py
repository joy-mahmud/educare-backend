from rest_framework import serializers
from .models import AcademicClass
class AcademicClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicClass
        fields = "__all__"

from rest_framework import serializers
from .models import ClassSubject


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
