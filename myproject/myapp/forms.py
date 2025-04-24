from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Coach, Profile, Training

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full p-2 rounded bg-black border border-gray-700 text-white',
                'placeholder': 'Nom d’utilisateur'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'w-full p-2 rounded bg-black border border-gray-700 text-white',
                'placeholder': 'Mot de passe'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'w-full p-2 rounded bg-black border border-gray-700 text-white',
                'placeholder': 'Confirmez le mot de passe'
            }),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age', 'height', 'weight', 'gender']
        widgets = {
            'age': forms.NumberInput(attrs={
                'class': 'w-full p-2 rounded bg-black border border-gray-700 text-white',
                'min': '0',
                'placeholder': 'Âge'
            }),
            'height': forms.NumberInput(attrs={
                'class': 'w-full p-2 rounded bg-black border border-gray-700 text-white',
                'min': '0',
                'placeholder': 'Taille (en cm)'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'w-full p-2 rounded bg-black border border-gray-700 text-white',
                'min': '0',
                'placeholder': 'Poids (en kg)'
            }),
            'gender': forms.Select(attrs={
                'class': 'w-full p-2 rounded bg-black border border-gray-700 text-white'
            }),
        }


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-2 rounded bg-black border border-gray-700 text-white',
        'placeholder': 'Nom d’utilisateur'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full p-2 rounded bg-black border border-gray-700 text-white',
        'placeholder': 'Mot de passe'
    }))


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = [
            'training_name',
            'training_type',
            'training_duration',
            'training_calories',
            'training_date',
            'goal',
            'level',
        ]
        widgets = {
            'training_name': forms.TextInput(attrs={
                'class': 'w-full p-2 rounded bg-black border border-gray-700 text-white',
                'placeholder': 'Nom de l’entraînement'
            }),
            'training_type': forms.Select(attrs={
                'class': 'w-full p-2 rounded bg-black border border-gray-700 text-white'
            }),
            'training_duration': forms.NumberInput(attrs={
                'class': 'w-full p-2 rounded bg-black border border-gray-700 text-white',
                'placeholder': 'Durée (min)'
            }),
            'training_calories': forms.NumberInput(attrs={
                'class': 'w-full p-2 rounded bg-black border border-gray-700 text-white',
                'placeholder': 'Calories estimées'
            }),
            'training_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full p-2 rounded bg-black border border-gray-700 text-white'
            }),
            'goal': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full p-2 rounded bg-black border border-gray-700 text-white',
                'placeholder': 'Objectif'
            }),
            'level': forms.Select(attrs={
                'class': 'w-full p-2 rounded bg-black border border-gray-700 text-white'
            }),
        }

class CoachForm(forms.ModelForm):
    class Meta:
        model = Coach
        fields = ['user', 'specialties', 'name', 'experience_years']