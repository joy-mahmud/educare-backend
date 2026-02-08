from django.db import models
from students.models import Student

# Create your models here.
class AcademicClass(models.Model):
    name = models.CharField(max_length=50)   # e.g. "6", "7", "8", "9", "10"

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=50)  # Science / Commerce / Arts

    def __str__(self):
        return self.name
    
class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ClassSubject(models.Model):
    SUBJECT_TYPE_CHOICES = (
        ("COMPULSORY", "Compulsory"),
        ("GROUP_COMPULSORY", "Group Compulsory"),
        ("ELECTIVE", "Elective"),
    )

    academic_class = models.ForeignKey(AcademicClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)

    subject_type = models.CharField(
        max_length=20,
        choices=SUBJECT_TYPE_CHOICES
    )

    def __str__(self):
        return f"{self.academic_class} - {self.subject}"

class StudentSubject(models.Model):
    SUBJECT_ROLE_CHOICES = (
        ("MAIN", "Main"),
        ("ELECTIVE", "Elective"),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class_subject = models.ForeignKey(
        ClassSubject,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=10,
        choices=SUBJECT_ROLE_CHOICES,
        default="MAIN"
    )

    def __str__(self):
        return f"{self.student} - {self.class_subject.subject}"

class StudentResult(models.Model):
    student_subject = models.ForeignKey(
            StudentSubject,
            on_delete=models.CASCADE
        )
    exam = models.CharField(max_length=100)

    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=5, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)





