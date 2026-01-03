from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt
from teachers.models import Teacher

class StudentJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        # No header → let permission handle it
        if not auth_header:
            return None

        try:
            token = auth_header.split(' ')[1]
            print(token)
        except IndexError:
            raise AuthenticationFailed('Invalid Authorization header format')

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        from students.models import Student
        student = Student.objects.filter(id=payload.get('student_id')).first()

        if not student:
            raise AuthenticationFailed('Student not found')

        return (student, None)

class TeacherJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None  # let permission handle it

        try:
            prefix, token = auth_header.split(" ")
            if prefix.lower() != "bearer":
                raise AuthenticationFailed("Invalid token prefix")
        except ValueError:
            raise AuthenticationFailed("Invalid Authorization header format")

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        teacher_id = payload.get("teacher_id")
        if not teacher_id:
            raise AuthenticationFailed("Invalid token payload")

        try:
            teacher = Teacher.objects.get(id=teacher_id)
        except Teacher.DoesNotExist:
            raise AuthenticationFailed("Teacher not found")

        # Attach teacher to request
        request.teacher = teacher

        # DRF expects (user, auth) tuple
        return (teacher, token)