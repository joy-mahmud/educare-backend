from rest_framework import serializers
from .models import Student
from academics.serializers import AcademicClassSerializer

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
class AllStudentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"

class StudentsAccordingClassSerializer(serializers.ModelSerializer):
    academic_class = AcademicClassSerializer(read_only=True)
    class Meta:
        model = Student
        fields = "__all__"