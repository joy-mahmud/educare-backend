from rest_framework import serializers
from .models import StudentAuth,TeacherAuth
from students.models import Student
from teachers.models import Teacher

class SetPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(min_length = 6)

    def validate_phone(self,value):
        if not Student.objects.filter(mobile = value).exists():
            raise serializers.ValidationError("you are not registered with this number")
        return value
    
    def save(self):
        phone = self.validated_data['phone']
        password = self.validated_data['password']

        student = Student.objects.get(mobile = phone)

        auth,created = StudentAuth.objects.get_or_create(student=student,phone=phone)

        auth.set_password(password)

        return auth
    
class StudentLoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        phone = data['phone']
        password = data['password']
        
        try:
            auth = StudentAuth.objects.get(phone=phone)
        except StudentAuth.DoesNotExist:
            serializers.ValidationError("Please set password first")
        
        if not auth.checking_password(password):
            raise serializers.ValidationError("Invalid password")
        
        data['auth'] = auth
        return data
class TeacherRegistrationSerializer(serializers.ModelSerializer):
    teacherId = serializers.CharField(write_only=True)  # input from API
    password = serializers.CharField(write_only=True)   # input from API

    # Optional: allow updating teacher fields
    name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    dateOfBirth = serializers.DateField(required=False)

    class Meta:
        model = TeacherAuth
        fields = ["teacherId", "email", "password", "name", "phone", "dateOfBirth"]

    def validate_teacherId(self, value):
        try:
            teacher = Teacher.objects.get(teacherId=value)
        except Teacher.DoesNotExist:
            raise serializers.ValidationError("Invalid teacher ID")

        # Ensure teacher hasn't registered yet
        if hasattr(teacher, "auth"):
            raise serializers.ValidationError("Teacher already registered")

        # Store teacher for create()
        self.context["teacher"] = teacher
        return value

    def create(self, validated_data):
        teacher = self.context["teacher"]
        email = validated_data["email"]
        password = validated_data["password"]

        # Update optional Teacher fields if provided
        for field in ["name", "phone", "dateOfBirth"]:
            if field in validated_data:
                setattr(teacher, field, validated_data[field])
        teacher.save()

        # Create TeacherAuth
        auth = TeacherAuth.objects.create(
            teacher=teacher,
            email=email,
        )
        auth.set_password(password)
        auth.save()
        return auth
    
class TeacherLoginSerializer(serializers.Serializer):
    teacherId = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            teacher = Teacher.objects.get(teacherId=data["teacherId"])
        except Teacher.DoesNotExist:
            raise serializers.ValidationError("Invalid teacher ID")

        if not hasattr(teacher, "auth"): # here auth is a related_name in the teacherAuth model
            raise serializers.ValidationError("Teacher not registered yet")

        auth = teacher.auth

        if not auth.check_password(data["password"]):
            raise serializers.ValidationError("Invalid password")

        data["auth"] = auth
        return data