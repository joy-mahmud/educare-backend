from django.db import models

class Student(models.Model):
    studentName = models.CharField(max_length=255)
    fatherName = models.CharField(max_length=255)
    motherName = models.CharField(max_length=255)
    presentAddress = models.TextField()
    permanentAddress = models.TextField()
    dateOfBirth = models.DateField()
    mobile = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    bloodGroup = models.CharField(max_length=10)
    religion = models.CharField(max_length=50)
    academicYear = models.CharField(max_length=20)
    classCode = models.CharField(max_length=20)
    sectionCode = models.CharField(max_length=20)
    groupCode = models.CharField(max_length=20)

    def __str__(self):
        return self.studentName

