from django import forms
from django.forms import ModelForm
from .models import Profile, Training

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full p-2 rounded bg-gray-900 border border-gray-700 text-white',
                'placeholder': 'Prénom'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full p-2 rounded bg-gray-900 border border-gray-700 text-white',
                'placeholder': 'Nom'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'w-full p-2 rounded bg-gray-900 border border-gray-700 text-white',
                'min': '0',
                'placeholder': 'Âge'
            }),
            'height': forms.NumberInput(attrs={
                'class': 'w-full p-2 rounded bg-gray-900 border border-gray-700 text-white',
                'min': '0',
                'placeholder': 'Taille (en cm)'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'w-full p-2 rounded bg-gray-900 border border-gray-700 text-white',
                'min': '0',
                'placeholder': 'Poids (en kg)'
            }),
            'gender': forms.Select(attrs={
                'class': 'w-full p-2 rounded bg-gray-900 border border-gray-700 text-white'
            }),
        }
class TrainingForm(ModelForm):
    class Meta:
        model = Training
        fields = "__all__"
        widgets = {
            'training_name': forms.TextInput(attrs={
                'class': 'w-full p-2 rounded bg-gray-900 border border-gray-700 text-white'
            }),
            'training_type': forms.Select(attrs={
                'class': 'w-full p-2 rounded bg-gray-900 border border-gray-700 text-white'
            }),
            'training_duration': forms.NumberInput(attrs={
                'class': 'w-full p-2 rounded bg-gray-900 border border-gray-700 text-white'
            }),
            'training_calories': forms.NumberInput(attrs={
                'class': 'w-full p-2 rounded bg-gray-900 border border-gray-700 text-white'
            }),
            'training_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full p-2 rounded bg-gray-900 border border-gray-700 text-white'
            }),
            'goal': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full p-2 rounded bg-gray-900 border border-gray-700 text-white'
            }),
            'level': forms.TextInput(attrs={
                'class': 'w-full p-2 rounded bg-gray-900 border border-gray-700 text-white'
            }),
        }
