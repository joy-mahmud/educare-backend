from django.db import models

class Student(models.Model):
    studentName = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, blank=True, null=True)

    fatherName = models.CharField(max_length=255)
    motherName = models.CharField(max_length=255)

    guardianName = models.CharField(max_length=255, blank=True, null=True)
    guardianMobile = models.CharField(max_length=20, blank=True, null=True)

    presentAddress = models.TextField()
    permanentAddress = models.TextField()

    nationality = models.CharField(max_length=100, blank=True, null=True)
    dateOfBirth = models.DateField()

    maritalStatus = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=20)
    bloodGroup = models.CharField(max_length=10)
    religion = models.CharField(max_length=50)

    academicYear = models.CharField(max_length=20)
    course = models.CharField(max_length=100, blank=True, null=True)

    honsRollNo = models.CharField(max_length=50, blank=True, null=True)
    honsRegNo = models.CharField(max_length=50, blank=True, null=True)
    honsPassingYear = models.CharField(max_length=10, blank=True, null=True)

    honsObtainedMarks = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    honsTotalMarks = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    createdAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.studentName


