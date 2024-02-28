from django.contrib import admin

from .models import Group, ExamGrade, Course, Category


admin.site.register(Group)
admin.site.register(Course)
admin.site.register(ExamGrade)
admin.site.register(Category)

