from django.http import JsonResponse

def profile_info(request, first_name):
    return JsonResponse({"message": f"Profil de {first_name}"})
