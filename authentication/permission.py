from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser


class IsStudentAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user is not None
            and not isinstance(request.user, AnonymousUser)
        )
class IsAdminTeacher(BasePermission):
    message = "Only admin teachers are allowed to access this resource."
    def has_permission(self, request, view):
        teacher = getattr(request, "teacher", None)
        return bool(teacher and teacher.role == "admin")