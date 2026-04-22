def analyze_symptoms(text):
    text = text.lower()

    severe = ["chest pain", "breathing issue", "high fever", "fatigue"]
    mild = ["cough", "cold", "headache", "fever"]

    score = 0

    for s in severe:
        if s in text:
            score += 2

    for m in mild:
        if m in text:
            score += 1

    if score >= 6:
        return "Severe Risk", 90
    elif score >= 3:
        return "Moderate Risk", 70
    else:
        return "Low Risk", 50