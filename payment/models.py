from django.db import models
from students.models import Student
# Create your models here.

class Payment(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    
    phoneNumber = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    payment_breakdown = models.JSONField(null=True,blank=True) 
    transactionId = models.CharField(max_length=100)
    paymentMethod = models.CharField(max_length=50)
    createdAt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,default='pending')
    slip = models.ForeignKey(
    "PaymentSlip",
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="payments"
    )
    
    def __str__(self):
        return f"{self.student.studentName} - {self.amount}"  
class PaymentSlip(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()

    memo_number = models.CharField(max_length=30, unique=True)

    total_paid = models.DecimalField(max_digits=10, decimal_places=2)
    total_payable = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2)

    breakdown = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.memo_number