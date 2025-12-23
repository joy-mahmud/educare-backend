from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display=("name","teacherId","phone","role","dateOfBirth")
    list_filter = ("role",)
    search_fields =("name","teacherId","phone")
    readonly_fields = ("teacherId",)
