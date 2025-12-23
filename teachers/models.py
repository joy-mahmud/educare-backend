from django.db import models

import random
from django.db import models, IntegrityError, transaction

def generate_8_digit_id():
    return str(random.randint(10_000_000, 99_999_999))

class Teacher(models.Model):

    ROLE_CHOICES = (
        ("teacher", "Teacher"),
        ("admin", "Admin"),
        ("staff", "Staff"),
    )

    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200,blank=True,null=True)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="teacher"
    )

    teacherId = models.CharField(
        max_length=8,
        unique=True,
        editable=False,
        db_index=True
    )
    dateOfBirth = models.DateField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        if self.teacherId:
            return super().save(*args, **kwargs)

        for _ in range(5):
            self.teacherId = generate_8_digit_id()
            try:
                with transaction.atomic():
                    return super().save(*args, **kwargs)
            except IntegrityError:
                self.teacherId = None

        raise ValueError("Could not generate unique teacherId")

    def __str__(self):
        return f"{self.name} ({self.teacherId})"