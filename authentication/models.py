from django.db import models
from students.models import Student
from django.contrib.auth.hashers import check_password,make_password
from teachers.models import Teacher
# Create your models here.
class StudentAuth(models.Model):
    student=models.OneToOneField(Student,on_delete=models.CASCADE)
    phone=models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=255,null=True,blank=True)
    
    def set_password(self,raw_password):
        self.password = make_password(raw_password)
        self.save()
    
    def checking_password(self,raw_password):
        return check_password(raw_password,self.password)
    
    def __str__(self):
        return self.phone
class TeacherAuth(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, related_name="auth")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.teacher.name} ({self.teacher.teacherId})"
