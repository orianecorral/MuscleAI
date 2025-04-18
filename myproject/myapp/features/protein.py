def protein_intake(weight: float, activity_level: str) -> float:
    if activity_level == 'sedentary':
        return weight * 0.8
    elif activity_level == 'active':
        return weight * 1.2
    elif activity_level == 'athlete':
        return weight * 1.6
    else:
        raise ValueError("Invalid activity level. Choose from 'sedentary', 'active', or 'athlete'.")