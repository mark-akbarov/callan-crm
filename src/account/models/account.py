import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from core.utils.base_model import BaseModel


class UserType(models.TextChoices):
    ADMIN = "Admin"
    TEACHER = "O'qituvchi"
    STUDENT = "O'quvchi"


class KnowledgeLevel(models.TextChoices):
    BEGINNER = "Boshlang'ich"
    ELEMENTARY = "O'rta"
    INTERMEDIATE = "Yuqori"


class User(AbstractUser):
    username = models.CharField(max_length=255, default=uuid.uuid4, unique=True, null=True)
    type = models.CharField(choices=UserType.choices, max_length=15)
    phone_number = models.CharField(max_length=25, unique=True)    
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    telegram_username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    telegram_user_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    
    REQUIRED_FIELDS = ['phone_number']
    
    def __str__(self):
        return f"{self.first_name}"

    class Meta:
        ordering = ('-date_joined',)
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "user"


class Enrollment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='enrollments')
    knowledge_level = models.CharField(max_length=255, choices=KnowledgeLevel.choices)
    
    def __str__(self):
        return f"{self.user} -> {self.course}"
    
