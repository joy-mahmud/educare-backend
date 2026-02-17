from rest_framework import serializers
from .models import AcademicClass
class AcademicClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicClass
        fields = "__all__"