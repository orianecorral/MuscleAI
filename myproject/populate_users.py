from django.contrib.auth.models import User
from myapp.models import Profile

users_data = [
    {"username": "clarisse", "password": "clarisse123", "first_name": "Clarisse", "last_name": "Lin", "age": 25, "height": 172, "weight": 75, "gender": "female"},
    {"username": "michael", "password": "michael123", "first_name": "Michael", "last_name": "Cooper", "age": 27, "height": 180, "weight": 70, "gender": "male"},
    {"username": "erica", "password": "erica123", "first_name": "Erica", "last_name": "Watson", "age": 54, "height": 165, "weight": 50, "gender": "female"},
    {"username": "david", "password": "david123", "first_name": "David", "last_name": "Glover", "age": 35, "height": 175, "weight": 72, "gender": "male"},
    {"username": "christina", "password": "christina123", "first_name": "Christina", "last_name": "Hays", "age": 45, "height": 160, "weight": 60, "gender": "female"},
    {"username": "angela", "password": "angela123", "first_name": "Angela", "last_name": "Miller", "age": 40, "height": 168, "weight": 65, "gender": "female"},
    {"username": "john", "password": "john123", "first_name": "John", "last_name": "Smith", "age": 30, "height": 183, "weight": 85, "gender": "male"},
    {"username": "sophia", "password": "sophia123", "first_name": "Sophia", "last_name": "Johnson", "age": 22, "height": 162, "weight": 55, "gender": "female"},
    {"username": "daniel", "password": "daniel123", "first_name": "Daniel", "last_name": "Brown", "age": 33, "height": 177, "weight": 78, "gender": "male"},
    {"username": "emily", "password": "emily123", "first_name": "Emily", "last_name": "Davis", "age": 29, "height": 165, "weight": 60, "gender": "female"},
]

for data in users_data:
    user, created = User.objects.get_or_create(username=data["username"])
    if created:
        user.set_password(data["password"])
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.save()
        print(f"✅ Utilisateur créé : {user.username}")
    else:
        print(f"ℹ️ Utilisateur déjà existant : {user.username}")

    # Supprimer profil existant pour recréer proprement
    Profile.objects.filter(user=user).delete()

    profile = Profile.objects.create(
        user=user,
        age=data["age"],
        height=data["height"],
        weight=data["weight"],
        gender=data["gender"]
    )
    print(f"🔗 Profil lié à : {user.username}")
