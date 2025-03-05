from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Profile
from .forms import ProfileForm
from django.shortcuts import render, redirect
from django.urls import reverse

def home_page(request):
    return render(request, 'home.html')

# need to implement either authentification or change url view
def profile_info(request, first_name):
    profile = get_object_or_404(Profile, first_name=first_name)
    context = {}
    context["profiles"] = {
        "first_name": profile.first_name,
        "last_name": profile.last_name,
        "age": profile.age,
        "height": profile.height,
        "weight": profile.weight,
        "gender": profile.gender,
    }
    
    return render(request, "profile_info.html", context)


def profile_show(request):
    context = {}
    context ["profiles"] = Profile.objects.all()
    return render(request, 'profile_show.html', context)

def profile_create_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save()
            return redirect(reverse('profile_info', args=[profile.first_name]))  
    else:
        form = ProfileForm()

    return render(request, 'profile_create.html', {'form': form})

def profile_update(request, first_name):
    profile = get_object_or_404(Profile, first_name=first_name)
    form = ProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('profile_info', args=[profile.first_name])) 
    
    context = {'form': form, 'profile': profile}
    return render(request, 'profile_update.html', context)

def profile_delete(request, first_name):
    profile = get_object_or_404(Profile, first_name=first_name)

    if request.method == 'POST':
        profile.delete()
        return redirect(reverse('home_page'))  

    context = {'profile': profile}
    return render(request, 'profile_delete.html', context)

