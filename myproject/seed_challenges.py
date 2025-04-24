from myapp.models import Challenge  # adapte si ton app s'appelle autrement
from django.contrib.auth.models import User
from datetime import date, timedelta
import random

# Utilisateurs connus
usernames = [
    "Clarisse Lin", "Michael Cooper", "David Glover", "Christina Hays",
    "Angela Miller", "John Smith", "Daniel Brown", "Emily Davis", "Erica Watson"
]

# Récupération des utilisateurs existants
users = list(User.objects.filter(username__in=usernames))
print(f"{len(users)} utilisateurs trouvés :", [u.username for u in users])

# Données des challenges
challenge_data = [
    ("Squat Queen", "Atteins ton PR au back squat en 6 semaines."),
    ("Deadlift Duel", "Affronte tes amis pour lever le plus de poids au deadlift."),
    ("Pushup Perfection", "100 pompes par jour pendant 30 jours."),
    ("Run & Burn", "Coure 50 km en un mois."),
    ("Cardio Clash", "10 sessions de HIIT en 2 semaines."),
    ("Flex Friday", "5 entraînements de haut du corps tous les vendredis."),
    ("Legs of Steel", "Challenge jambes : squat + fente 3x/semaine."),
    ("Bench Beast", "Progresse ton bench de +10kg en 8 semaines."),
    ("Core Crusher", "20 minutes d’abdos chaque jour."),
    ("Iron March", "Augmente tes PR sur les trois grands lifts.")
]

# Création des challenges
for name, description in challenge_data:
    start = date.today() - timedelta(days=random.randint(0, 10))
    end = start + timedelta(days=random.randint(20, 60))

    challenge = Challenge.objects.create(
        name=name,
        description=description,
        start_date=start,
        end_date=end,
    )

    if len(users) >= 3:
        k = random.randint(3, min(6, len(users)))
    elif users:
        k = len(users)
    else:
        k = 0

    participants = random.sample(users, k=k) if k > 0 else []
    challenge.participants.set(participants)

    classement = {str(i + 1): user.username for i, user in enumerate(participants)}
    challenge.classement = classement
    challenge.save()

print("✅ 10 challenges générés avec succès dans myapp 🎉")
