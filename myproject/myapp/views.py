from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q

from myapp.features.bmi import bmi_category, calculate_bmi
from myapp.features.calories import calculate_bmr, calculate_tdee
from myapp.features.combined import run_all_calculations
from myapp.features.protein import protein_intake
from .models import Profile, Training
from .forms import ProfileForm, TrainingForm
from django.contrib.auth.forms import UserCreationForm


import random

User = get_user_model()

# ===================== Pages Générales =====================
def homepage(request):
    trainings = Training.objects.all()
    recherche = ''
    selected_types = []
    selected_levels = []

    types_list = Training.TYPE_CHOICES
    levels_list = Training.LEVEL_CHOICES

    result = None
    error_message = None

    if request.method == 'POST':
        if 'recherche' in request.POST:
            recherche = request.POST.get('recherche', '').strip()
            selected_types = request.POST.getlist('types')
            selected_levels = request.POST.getlist('levels')

            filters = Q()

            if recherche:
                filters &= (
                    Q(training_name__icontains=recherche) |
                    Q(training_type__icontains=recherche) |
                    Q(goal__icontains=recherche)
                )

            if selected_types:
                filters &= Q(training_type__in=selected_types)

            if selected_levels:
                filters &= Q(level__in=selected_levels)

            trainings = Training.objects.filter(filters)

        elif 'gender' in request.POST:
            try:
                gender = request.POST.get('gender')
                weight = float(request.POST.get('weight'))
                height = float(request.POST.get('height'))
                age = int(request.POST.get('age'))
                activity = request.POST.get('activity')

                result = run_all_calculations(gender, weight, height, age, activity)
            except (ValueError, TypeError) as e:
                error_message = f"Erreur dans le formulaire : {str(e)}"

    image_list = [f'assets/images/gym{i}.jpg' for i in range(1, 10)]
    training_data = [
        {
            'training': training,
            'image': random.choice(image_list)
        } for training in trainings
    ]

    return render(request, 'home.html', {
        'training_data': training_data,
        'recherche': recherche,
        'selected_types': selected_types,
        'selected_levels': selected_levels,
        'types_list': types_list,
        'levels_list': levels_list,
        'result': result,
        'error_message': error_message,
    })

# ===================== Profils =====================
def profile_info(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    return render(request, "profiles/profile_info.html", {"profile": profile})

def profile_show(request):
    context = {"profiles": Profile.objects.all()}
    return render(request, 'profiles/profile_show.html', context)

def profile_create_view(request):
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()  # plus besoin de set_password !
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return redirect(reverse('profile_info', args=[profile.pk]))
    else:
        user_form = UserCreationForm()
        profile_form = ProfileForm()

    return render(request, 'profiles/profile_create.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

def profile_update(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('profile_info', args=[profile.pk]))

    return render(request, 'profiles/profile_update.html', {'form': form, 'profile': profile})

def profile_delete(request, pk):
    profile = get_object_or_404(Profile, pk=pk)

    if request.method == 'POST':
        profile.delete()
        return redirect(reverse('homepage'))

    return render(request, 'profiles/profile_delete.html', {'profile': profile})

# ===================== Trainings =====================
def training_info(request, pk):
    training = get_object_or_404(Training, pk=pk)
    return render(request, 'trainings/training_info.html', {"training": training})

def training_show(request):
    trainings = Training.objects.all()
    image_list = [f'assets/images/gym{i}.jpg' for i in range(1, 10)]
    training_data = [
        {
            'training': training,
            'image': random.choice(image_list)
        } for training in trainings
    ]
    return render(request, 'trainings/training_show.html', {'training_data': training_data})

def training_create_view(request):
    if request.method == "POST":
        form = TrainingForm(request.POST)
        if form.is_valid():
            training = form.save()
            return redirect(reverse('training_info', args=[training.pk]))
    else:
        form = TrainingForm()

    return render(request, 'trainings/training_create.html', {'form': form})

def training_update(request, pk):
    training = get_object_or_404(Training, pk=pk)

    if request.method == 'POST':
        form = TrainingForm(request.POST, instance=training)
        if form.is_valid():
            form.save()
            return redirect(reverse('training_info', args=[training.pk]))
    else:
        form = TrainingForm(instance=training)

    return render(request, 'trainings/training_update.html', {'form': form, 'training': training})

def training_delete(request, pk):
    training = get_object_or_404(Training, pk=pk)

    if request.method == 'POST':
        training.delete()
        return redirect(reverse('training_show'))

    return render(request, 'trainings/training_delete.html', {'training': training})

# ===================== Calculators =====================
def bmi_view(request):
    bmi = None
    category = None

    if request.method == 'POST':
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        bmi = calculate_bmi(weight, height)
        category = bmi_category(bmi)

    return render(request, 'calculators/bmi.html', {'bmi': bmi, 'category': category})

def protein_view(request):
    protein = None
    error_message = None

    if request.method == 'POST':
        weight = request.POST.get('weight')
        activity_level = request.POST.get('activity_level')
        try:
            protein = protein_intake(float(weight), activity_level)
        except ValueError as e:
            error_message = str(e)

    return render(request, 'calculators/protein.html', {'protein': protein, 'error_message': error_message})

def calories_view(request):
    calories = None
    error_message = None

    if request.method == 'POST':
        gender = request.POST.get('gender')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        age = request.POST.get('age')
        activity = request.POST.get('activity')

        try:
            bmr = calculate_bmr(gender, float(weight), float(height), int(age))
            calories = calculate_tdee(bmr, activity)
        except ValueError as e:
            error_message = str(e)

    return render(request, 'calculators/calories.html', {
        'calories': calories,
        'error_message': error_message
    })

def combined_view(request):
    result = None
    error_message = None

    if request.method == 'POST':
        try:
            gender = request.POST.get('gender')
            weight = float(request.POST.get('weight'))
            height = float(request.POST.get('height'))
            age = int(request.POST.get('age'))
            activity = request.POST.get('activity')
            result = run_all_calculations(gender, weight, height, age, activity)
        except (ValueError, TypeError) as e:
            error_message = f"Erreur dans le formulaire : {str(e)}"

    return render(request, 'calculators/combined.html', {
        'result': result,
        'error_message': error_message
    })

# ===================== Auth =====================
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print("📥 Tentative de login :")
        print("  username =", username)
        print("  password =", password)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            print("✅ Connexion réussie :", user)
            login(request, user)
            messages.success(request, f"Connexion réussie. Bienvenue {user.username} !")
            return redirect('homepage')
        else:
            print("❌ Échec d'authentification pour :", username)
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('homepage')  # ← NOM de la route, pas un fichier
