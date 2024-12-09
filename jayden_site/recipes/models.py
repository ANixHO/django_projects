from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class Recipe(models.Model):
    name=models.CharField(max_length=200, validators=[MinLengthValidator(5,"Recipe name must contain at least 5 characters")])
    rating=models.PositiveIntegerField()
    detail=models.TextField(max_length=500)

    def __str__(self):
        return self.name