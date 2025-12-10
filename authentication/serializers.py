from rest_framework import serializers
from .models import StudentAuth 
from students.models import Student

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