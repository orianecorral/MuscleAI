def calculate_bmi(weight, height_cm):
    try:
        height_m = float(height_cm) / 100  # conversion cm → m
        bmi = float(weight) / (height_m ** 2)
        return round(bmi, 2)
    except ZeroDivisionError:
        return "Height cannot be zero"
    except ValueError:
        return "Invalid input"

def bmi_category(bmi):
    if isinstance(bmi, str):
        return bmi
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"
