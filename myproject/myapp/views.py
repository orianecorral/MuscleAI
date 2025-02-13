from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Profile
from .forms import ProfileForm
from django.shortcuts import render, redirect

def profile_info(request, first_name):
    """
    Récupère un profil via son prénom et retourne ses informations en JSON.
    """
    profile = get_object_or_404(Profile, first_name=first_name)
    data = {
        "first_name": profile.first_name,
        "last_name": profile.last_name,
        "age": profile.age,
        "height": profile.height,
        "weight": profile.weight,
        "gender": profile.gender,
    }
    return JsonResponse(data)


def profile_create_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile_success')  # Replace with your success page
    else:
        form = ProfileForm()

    return render(request, 'profile_create.html', {'form': form})
