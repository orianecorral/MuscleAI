def calculate_bmr(gender: str, weight: float, height: float, age: int) -> float:
    if gender == 'male':
        return 66.5 + (13.75 * weight) + (5.003 * height) - (6.775 * age)
    elif gender == 'female':
        return 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)
    else:
        raise ValueError("Genre invalide : 'male' ou 'female' attendus.")

def calculate_tdee(bmr: float, activity_level: str) -> float:
    factors = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    if activity_level not in factors:
        raise ValueError("Niveau d'activité invalide.")
    return round(bmr * factors[activity_level], 2)
