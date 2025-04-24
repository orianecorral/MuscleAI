from django.db import models
from django.forms import ModelForm
import uuid 
from django.contrib.auth import get_user_model
User = get_user_model()

class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialties = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    experience_years = models.IntegerField()

    def __str__(self):
        return f"Coach: {self.user.username}"
class Profile(models.Model):
    GENDER_CHOICES = (
        ("female", "Female"),
        ("male", "Male"),
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # 👈 ajout
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)
    coach = models.ForeignKey(Coach, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')



    # Infos personnelles
    age = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)  # en cm
    weight = models.IntegerField(null=True, blank=True)  # en kg
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="female", null=True, blank=True)
    is_connected = models.BooleanField(default=False)

    # Résultats calculés (en cache, pour éviter de recalculer à chaque affichage)
    bmi = models.FloatField(null=True, blank=True)
    daily_protein_requirement = models.FloatField(null=True, blank=True)  # en g
    daily_calories_estimate = models.FloatField(null=True, blank=True)   # en kcal

    def __str__(self):
        return f"{self.user.username} ({self.user.first_name} {self.user.last_name})"

    def calculate_bmi(self):
        if self.height and self.weight:
            height_m = self.height / 100
            return round(self.weight / (height_m ** 2), 2)
        return None

    def calculate_protein(self):
        # à adapter selon ton modèle : ici 1.6g/kg comme exemple sportif
        if self.weight:
            return round(self.weight * 1.6, 2)
        return None

    def calculate_calories(self):
        if self.weight and self.height and self.age and self.gender:
            if self.gender == "male":
                return round(10 * self.weight + 6.25 * self.height - 5 * self.age + 5)
            else:
                return round(10 * self.weight + 6.25 * self.height - 5 * self.age - 161)
        return None

    def update_metrics(self):
        self.bmi = self.calculate_bmi()
        self.daily_protein_requirement = self.calculate_protein()
        self.daily_calories_estimate = self.calculate_calories()
        self.save()

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
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="trainings", null=True, blank=True)
    training_name = models.CharField(max_length=200)
    training_type = models.CharField(max_length=200, choices = TYPE_CHOICES)
    training_duration = models.IntegerField()
    training_calories = models.IntegerField()
    training_date = models.DateField()
    goal= models.TextField()
    level = models.CharField(max_length=200, choices = LEVEL_CHOICES)
    

    class Meta:
        db_table = 'training'
        managed = True  # Important pour dire à Django de ne pas toucher la table

    def __str__(self):
        return self.training_name

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_friend_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_friend_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user.username} → {self.to_user.username} [{self.status}]"

class Challenge(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    participants = models.ManyToManyField(User, related_name='challenges', blank=True)
    classement = models.JSONField(blank=True, null=True)  # JSON > Text pour les classements structurés

    def __str__(self):
        return self.name

    def is_active(self):
        from django.utils.timezone import now
        return self.start_date <= now().date() <= self.end_date
