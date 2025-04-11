from django import forms
from django.forms import ModelForm
from .models import Profile, Training

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"  # Inclut tous les champs du modèle Profile

class TrainingForm(ModelForm):
    class Meta:
        model = Training
        fields = "__all__"  # Inclut tous les champs du modèle Training