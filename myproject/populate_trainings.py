from myapp.models import Training
from datetime import date, timedelta

trainings_data = [
    {"training_name": "Morning Cardio Blast", "training_type": "Cardio", "training_duration": 45, "training_calories": 400, "training_date": date.today() - timedelta(days=1)},
    {"training_name": "Upper Body Strength", "training_type": "Musculation", "training_duration": 60, "training_calories": 500, "training_date": date.today() - timedelta(days=2)},
    {"training_name": "Leg Day Challenge", "training_type": "Musculation", "training_duration": 75, "training_calories": 600, "training_date": date.today() - timedelta(days=3)},
    {"training_name": "Yoga Flow", "training_type": "Yoga", "training_duration": 40, "training_calories": 200, "training_date": date.today() - timedelta(days=4)},
    {"training_name": "HIIT Burner", "training_type": "HIIT", "training_duration": 30, "training_calories": 350, "training_date": date.today() - timedelta(days=5)},
    {"training_name": "Pilates Core", "training_type": "Pilates", "training_duration": 50, "training_calories": 300, "training_date": date.today() - timedelta(days=6)},
    {"training_name": "Back and Biceps", "training_type": "Musculation", "training_duration": 65, "training_calories": 550, "training_date": date.today() - timedelta(days=7)},
    {"training_name": "Evening Run", "training_type": "Cardio", "training_duration": 55, "training_calories": 450, "training_date": date.today() - timedelta(days=8)},
    {"training_name": "Mobility Routine", "training_type": "Mobilité", "training_duration": 35, "training_calories": 180, "training_date": date.today() - timedelta(days=9)},
    {"training_name": "Full Body Circuit", "training_type": "Circuit Training", "training_duration": 60, "training_calories": 520, "training_date": date.today() - timedelta(days=10)},
]

for data in trainings_data:
    training, created = Training.objects.get_or_create(
        training_name=data["training_name"],
        training_type=data["training_type"],
        training_duration=data["training_duration"],
        training_calories=data["training_calories"],
        training_date=data["training_date"]
    )
    if created:
        print(f"✅ Training créé : {training.training_name}")
    else:
        print(f"ℹ️ Training déjà existant : {training.training_name}")
