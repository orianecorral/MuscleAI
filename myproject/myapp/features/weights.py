def calculate_percentage_load(pr: float, percentage: float) -> float:
    """
    Calcule la charge à utiliser à partir d’un PR et d’un pourcentage donné.
    Exemple : PR = 100kg, % = 80 → 80kg
    """
    if not 0 < percentage <= 100:
        raise ValueError("Le pourcentage doit être compris entre 0 et 100.")
    return round(pr * (percentage / 100), 2)
