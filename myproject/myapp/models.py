from django.db import models
from django.forms import ModelForm
from django.contrib.auth import get_user_model
User = get_user_model()

class Profile(models.Model):
    GENDER_CHOICES = (
        ("female", "Female"),
        ("male", "Male"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # ← suppression de null=True
    age = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="female")
    is_connected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} ({self.user.first_name} {self.user.last_name})"
    
class Training(models.Model):
    TYPE_CHOICES = (
        ("musculation", "Musculation"),
        ("cardio", "Cardio"),
        ("yoga", "Yoga"),
        ("hiit", "HIIT"),
        ("pilates", "Pilates"),
        ("mobilité", "Mobilité"),
        ("circuit training", "Circuit Training"),
        ("running", "Running"),
        ("streetlifting", "Streetlifting"),
    )

    LEVEL_CHOICES = (
        ("Débutant", "Débutant"),
        ("Intermédiaire", "Intermédiaire"),
        ("Avancé", "Avancé"),
        ("Tous niveaux", "Tous niveaux"),
    )

    training_name = models.CharField(max_length=200)
    training_type = models.CharField(max_length=200, choices = TYPE_CHOICES)
    training_duration = models.IntegerField()
    training_calories = models.IntegerField()
    training_date = models.DateField()
    goal= models.TextField()
    level = models.CharField(max_length=200, choices = LEVEL_CHOICES)
    

    class Meta:
        db_table = 'training'
        managed = False  # Important pour dire à Django de ne pas toucher la table

    def __str__(self):
        return self.training_name
