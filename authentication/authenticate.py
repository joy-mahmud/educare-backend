from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt

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
