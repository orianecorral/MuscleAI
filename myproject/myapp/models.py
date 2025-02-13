from django.db import models
from django.forms import ModelForm


class Profile(models.Model):
    GENDER_CHOICES = (
        ("female", "Female"),
        ("male", "Male"),
    )

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    age = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="female")  # Default set

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
