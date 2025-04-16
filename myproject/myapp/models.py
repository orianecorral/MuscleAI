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
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="female")  

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Training(models.Model):
    training_name = models.CharField(max_length=200)
    training_type = models.CharField(max_length=200)
    training_duration = models.IntegerField()
    training_calories = models.IntegerField()
    training_date = models.DateField()
    goal= models.TextField()
    level = models.CharField(max_length=200)
    

    class Meta:
        db_table = 'training'
        managed = False  # Important pour dire à Django de ne pas toucher la table

    def __str__(self):
        return self.training_name
