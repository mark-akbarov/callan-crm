from django.db import models

from core.utils.base_model import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'