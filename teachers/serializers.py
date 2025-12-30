from rest_framework import serializers
from .models import Teacher

class TeacherCreateSerializer(serializers.ModelSerializer):
    dateOfBirth = serializers.DateField(
    required=False,
    allow_null=True,
    input_formats=["%Y-%m-%d"]
    )
    subject = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )
    class Meta:
        model = Teacher
        fields = [
            "name",
            "phone",
            "subject",
            "role",
            "dateOfBirth",
        ]
        read_only_fields = ("teacherId",)

    def to_internal_value(self, data):
        data = data.copy()

        if data.get("dateOfBirth") == "":
            data["dateOfBirth"] = None

        if data.get("subject") == "":
            data["subject"] = None

        return super().to_internal_value(data)