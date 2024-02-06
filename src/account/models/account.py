import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from core.utils.base_model import BaseModel


class User(AbstractUser):
    username = models.CharField(max_length=255, default=uuid.uuid4, unique=True, null=True)
    phone_number = models.CharField(max_length=25, unique=True)    
    email = models.EmailField(max_length=255, unique=True, null=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    parent_name = models.CharField(max_length=255, null=True)
    parent_phone_number = models.CharField(max_length=25, unique=True, null=True)
    telegram_username = models.CharField(max_length=255, unique=True, null=True)
    telegram_user_id = models.PositiveIntegerField(unique=True, null=True)
    
    REQUIRED_FIELDS = ['phone_number']
    
    def __str__(self):
        return self.phone_number

    class Meta:
        ordering = ('-date_joined',)
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "user"


class Enrollment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='enrollments')
    knowledge_level = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.user} -> {self.course}"
    
