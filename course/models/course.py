from django.db import models
from core.utils.base_model import BaseModel


class Group(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    teacher = models.ForeignKey("account.User", on_delete=models.CASCADE, null=True)
    students = models.ManyToManyField("account.User", related_name="course_groups")
    def __str__(self) -> str:
        return self.name


class ExamGrade(BaseModel):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='exam_grades')
    date = models.DateField()
    grades_photo = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.group}  ({self.date})"


class Course(BaseModel):
    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(
        'account.User', 
        on_delete=models.CASCADE, 
        related_name='courses', 
        null=True
        )
    info = models.TextField()
    category = models.ForeignKey('course.Category', on_delete=models.CASCADE, related_name='courses')
    
    def __str__(self) -> str:
        return self.name

