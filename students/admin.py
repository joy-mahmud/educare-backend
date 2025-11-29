from django.contrib import admin
from .models import Student
# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'studentName', 'mobile')
    search_fields = ('studentName', 'mobile')
    list_filter = ('studentName',)
    ordering = ('id',)
