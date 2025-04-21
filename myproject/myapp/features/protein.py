def protein_intake(weight: float, activity_level: str) -> float:
    """Calcule l'apport en protéines recommandé (en grammes) selon le niveau d'activité"""
    levels = {
        'sedentary': 0.8,
        'light': 1.0,
        'moderate': 1.2,
        'active': 1.5,
        'very_active': 1.8,
        'athlete': 2.0,
    }

    if activity_level not in levels:
        raise ValueError(f"Niveau d'activité non reconnu : {activity_level}")

    return round(weight * levels[activity_level], 1)
