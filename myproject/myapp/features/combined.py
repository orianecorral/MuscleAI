from .bmi import calculate_bmi, bmi_category
from .protein import protein_intake
from .calories import calculate_bmr, calculate_tdee

def run_all_calculations(gender: str, weight: float, height: float, age: int, activity: str):
    bmi = calculate_bmi(weight, height)
    bmi_cat = bmi_category(bmi)
    proteins = protein_intake(weight, activity)
    bmr = calculate_bmr(gender, weight, height, age)
    calories = calculate_tdee(bmr, activity)

    return {
        "bmi": bmi,
        "bmi_category": bmi_cat,
        "proteins": proteins,
        "calories": calories
    }
