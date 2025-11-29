from django.db import models
from students.models import Student
# Create your models here.

class Payment(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    
    phoneNumber = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    transactionId = models.CharField(max_length=100)
    paymentMethod = models.CharField(max_length=50)
    createdAt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,default='pending')
    
    def __str__(self):
        return f"{self.student.studentName} - {self.amount}"  