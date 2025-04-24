from django.contrib.auth.models import User
from myapp.models import Coach  # adapte le nom de ton app si besoin

coaches_data = [
    {"username": "emma", "password": "emma123", "first_name": "Emma", "last_name": "Durand", "specialties": "Powerlifting, Hypertrophie", "experience": 5},
    {"username": "leo", "password": "leo123", "first_name": "Léo", "last_name": "Martin", "specialties": "CrossFit, Mobilité", "experience": 7},
    {"username": "nina", "password": "nina123", "first_name": "Nina", "last_name": "Bellec", "specialties": "Yoga, Pilates", "experience": 4},
    {"username": "mohamed", "password": "mohamed123", "first_name": "Mohamed", "last_name": "Ziane", "specialties": "Boxe, HIIT", "experience": 8},
    {"username": "lucie", "password": "lucie123", "first_name": "Lucie", "last_name": "Lefèvre", "specialties": "Cardio, Fitness", "experience": 3},
]

for data in coaches_data:
    user, created = User.objects.get_or_create(username=data["username"])
    if created:
        user.set_password(data["password"])
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.email = f"{data['username']}@coach.com"
        user.save()
        print(f"✅ Utilisateur créé : {user.username}")
    else:
        print(f"ℹ️ Utilisateur déjà existant : {user.username}")

    # Supprimer coach existant pour recréer proprement
    Coach.objects.filter(user=user).delete()

    coach = Coach.objects.create(
        user=user,
        name=f"{data['first_name']} {data['last_name']}",
        specialties=data["specialties"],
        experience_years=data["experience"]
    )
    print(f"🧑‍🏫 Coach créé : {coach.name}")
