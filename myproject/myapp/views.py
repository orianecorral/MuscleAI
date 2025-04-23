from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login, logout  # ✅ ajouté ici
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q

from myapp.features.bmi import bmi_category, calculate_bmi
from myapp.features.calories import calculate_bmr, calculate_tdee
from myapp.features.combined import run_all_calculations
from myapp.features.protein import protein_intake
from .models import FriendRequest, Profile, Training
from .forms import CustomUserCreationForm, ProfileForm, TrainingForm
from django.contrib.auth.forms import UserCreationForm


import random

User = get_user_model()


def profile_by_uuid(request, uuid):
    profile = get_object_or_404(Profile, uuid=uuid)
    profile.update_metrics()
    return render(request, "profiles/profile_info.html", {"profile": profile})


# ===================== Pages Générales =====================
@login_required
def homepage(request):
    # 🎯 Séparation des données
    public_trainings = Training.objects.filter(profile__isnull=True)
    user_trainings = Training.objects.filter(profile=request.user.profile)

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

            filters = Q(profile__isnull=True)  # filtrer uniquement les trainings publics

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

            public_trainings = Training.objects.filter(filters)

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

    # 🎨 Ajout d'images aléatoires pour les trainings publics
    image_list = [f'assets/images/gym{i}.jpg' for i in range(1, 10)]
    training_data = [
        {
            'training': training,
            'image': random.choice(image_list)
        } for training in public_trainings
    ]

    return render(request, 'home.html', {
        'training_data': training_data,
        'user_trainings': user_trainings,
        'recherche': recherche,
        'selected_types': selected_types,
        'selected_levels': selected_levels,
        'types_list': types_list,
        'levels_list': levels_list,
        'result': result,
        'error_message': error_message,
    })
# ===================== Profils =====================
@login_required
def my_profile_view(request):
    profile = request.user.profile
    return redirect('profile_info', uuid=profile.uuid)

@login_required
def profile_info_view(request, uuid):
    profile = get_object_or_404(Profile, uuid=uuid)
    is_own_profile = request.user.profile.uuid == profile.uuid

    trainings = Training.objects.filter(profile=profile)

    received_requests = FriendRequest.objects.filter(to_user=request.user, status='pending') if is_own_profile else None
    sent_requests = FriendRequest.objects.filter(from_user=request.user, status='pending') if is_own_profile else None

    context = {
        'profile': profile,
        'trainings': trainings,
        'received_requests': received_requests,
        'sent_requests': sent_requests,
        'is_own_profile': is_own_profile,
    }
    return render(request, 'profiles/profile_info.html', context)

@login_required
def profile_update(request, uuid):
    profile = get_object_or_404(Profile, uuid=uuid)
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_info', uuid=profile.uuid)

    return render(request, 'profiles/profile_update.html', {'form': form, 'profile': profile})

@login_required
def profile_delete(request, uuid):
    profile = get_object_or_404(Profile, uuid=uuid)

    if request.method == 'POST':
        profile.delete()
        return redirect('homepage')

    return render(request, 'profiles/profile_delete.html', {'profile': profile})

@login_required
def profile_show(request):
    user_profile = request.user.profile
    profiles = Profile.objects.exclude(uuid=user_profile.uuid)

    sent_requests = FriendRequest.objects.filter(from_user=request.user, status='pending')
    sent_to_uuids = [fr.to_user.profile.uuid for fr in sent_requests]

    friends_uuids = user_profile.friends.all().values_list('uuid', flat=True)

    context = {
        'profiles': profiles,
        'sent_to_uuids': sent_to_uuids,
        'friends_uuids': friends_uuids,
    }

    return render(request, 'profiles/profile_show.html', context)

@csrf_exempt
def profile_create_view(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('profile_info', uuid=profile.uuid)
    else:
        user_form = UserCreationForm()
        profile_form = ProfileForm()

    return render(request, 'profiles/profile_create.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

@login_required
def send_friend_request(request, uuid):
    to_profile = get_object_or_404(Profile, uuid=uuid)
    from_profile = request.user.profile

    if to_profile != from_profile:
        existing = FriendRequest.objects.filter(
            from_user=from_profile.user,
            to_user=to_profile.user,
            status='pending'
        ).exists()

        if not existing:
            FriendRequest.objects.create(
                from_user=from_profile.user,
                to_user=to_profile.user
            )
            messages.success(request, f"Demande envoyée à {to_profile.user.username} !")
        else:
            messages.info(request, f"Une demande est déjà en attente pour {to_profile.user.username}.")

    return redirect('profile_info', uuid=to_profile.uuid)

@login_required
def accept_friend_request(request, pk):
    friend_request = get_object_or_404(FriendRequest, pk=pk, to_user=request.user)

    if friend_request.status != 'pending':
        messages.warning(request, "Cette demande n'est plus valide.")
    else:
        friend_request.status = 'accepted'
        friend_request.save()

        from_profile = friend_request.from_user.profile
        to_profile = friend_request.to_user.profile

        from_profile.friends.add(to_profile)
        to_profile.friends.add(from_profile)

        messages.success(request, f"Tu es maintenant ami(e) avec {from_profile.user.username} !")

    return redirect('profile_info', uuid=request.user.profile.uuid)

@login_required
def reject_friend_request(request, pk):
    friend_request = get_object_or_404(FriendRequest, pk=pk, to_user=request.user)

    if friend_request.status != 'pending':
        messages.warning(request, "Cette demande n'est plus active.")
    else:
        friend_request.status = 'rejected'
        friend_request.save()
        messages.info(request, f"Demande de {friend_request.from_user.username} refusée.")

    return redirect('profile_info', uuid=request.user.profile.uuid)

# ===================== Trainings =====================
def training_info(request, pk):
    training = get_object_or_404(Training, pk=pk)
    return render(request, 'trainings/training_info.html', {"training": training})

@login_required
def training_show(request):
    trainings = Training.objects.filter(profile__isnull=True)
    user_profile = request.user.profile

    user_training_ids = Training.objects.filter(profile=user_profile).values_list('training_name', flat=True)

    image_list = [f'assets/images/gym{i}.jpg' for i in range(1, 10)]
    training_data = [
        {
            'training': training,
            'image': random.choice(image_list)
        } for training in trainings
    ]

    return render(request, 'trainings/training_show.html', {
        'training_data': training_data,
        'user_training_names': list(user_training_ids),
    })


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


@login_required
def add_training(request):
    if request.method == 'POST':
        form = TrainingForm(request.POST)
        if form.is_valid():
            training = form.save(commit=False)
            training.profile = request.user.profile
            training.save()
            return redirect('profile')  # ou vers un dashboard
    else:
        form = TrainingForm()
    return render(request, 'trainings/add_training.html', {'form': form})

@login_required
def add_training_to_profile(request, training_id):
    user_profile = request.user.profile

    # training public (non assigné à un profil)
    public_training = get_object_or_404(Training, id=training_id, profile__isnull=True)

    # Empêcher l’ajout en double (basé sur le nom du training déjà dans le profil)
    already_added = Training.objects.filter(profile=user_profile, training_name=public_training.training_name).exists()

    if already_added:
        messages.warning(request, "Ce training est déjà dans votre profil.")
    else:
        # Créer une copie liée à l'utilisateur
        Training.objects.create(
            training_name=public_training.training_name,
            training_type=public_training.training_type,
            training_duration=public_training.training_duration,
            training_calories=public_training.training_calories,
            training_date=public_training.training_date,
            goal=public_training.goal,
            level=public_training.level,
            profile=user_profile
        )
        messages.success(request, "Training ajouté avec succès à votre profil.")

    return redirect('profile_info', pk=request.user.profile.pk)  # ou autre URL