from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Profile, Training
from .forms import ProfileForm, TrainingForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q

import random


def homepage(request):
    trainings = Training.objects.all()
    recherche = None  # Pour afficher le mot-clé si recherche faite

    if request.method == 'POST':
        recherche = request.POST.get('recherche')
        if recherche:
            trainings = Training.objects.filter(
                Q(training_name__icontains=recherche) |
                Q(training_type__icontains=recherche) |
                Q(goal__icontains=recherche)
            )

    image_list = [f'assets/images/gym{i}.jpg' for i in range(1, 10)]
    training_data = [
        {
            'training': training,
            'image': random.choice(image_list)
        } for training in trainings
    ]

    return render(request, 'home.html', {
        'training_data': training_data,
        'recherche': recherche
    })
# Model Views
# need to implement either authentification or change url view
def profile_info(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    return render(request, "profiles/profile_info.html", {"profile": profile})


def profile_show(request):
    context = {}
    context ["profiles"] = Profile.objects.all()
    return render(request, 'profiles/profile_show.html', context)

def profile_create_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save()
            return redirect(reverse('profile_info', args=[profile.pk]))  
    else:
        form = ProfileForm()

    return render(request, 'profiles/profile_create.html', {'form': form})

def profile_update(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    form = ProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('profile_info', args=[profile.pk])) 
    
    context = {'form': form, 'profile': profile}
    return render(request, 'profiles/profile_update.html', context)

def profile_delete(request, pk):
    profile = get_object_or_404(Profile, pk=pk)

    if request.method == 'POST':
        profile.delete()
        return redirect(reverse('homepage'))  

    context = {'profile': profile}
    return render(request, 'profiles/profile_delete.html', context)



# Model Training

def training_info(request, pk):
    training = get_object_or_404(Training, pk=pk)
    context = {
        "training": training
    }
    return render(request, 'trainings/training_info.html', context)


def training_show(request):
    trainings = Training.objects.all()
    image_list = [f'assets/images/gym{i}.jpg' for i in range(1, 10)]  # gym1.jpg à gym9.jpg
    # Associer une image aléatoire à chaque training
    training_data = [
        {
            'training': training,
            'image': random.choice(image_list)
        } for training in trainings
    ]

    return render(request, 'trainings/training_show.html', {
        'training_data': training_data,
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
    
    context = {'form': form, 'training': training}
    return render(request, 'trainings/training_update.html', context)

def training_delete(request, pk):
    training = get_object_or_404(Training, pk=pk)

    if request.method == 'POST':
        training.delete()
        return redirect(reverse('training_show'))  

    context = {'training': training}
    return render(request, 'trainings/training_delete.html', context)