def recommend_fertilizer(soil_n, soil_p, soil_k):
    recommendations = []

    try:
        soil_n = float(soil_n)
        soil_p = float(soil_p)
        soil_k = float(soil_k)
    except (TypeError, ValueError):
        return []

    if soil_n < 50:
        recommendations.append({
            "nutrient": "Nitrogen",
            "fertilizer": "Urea",
            "reason": "Soil nitrogen level is low"
        })

    if soil_p < 40:
        recommendations.append({
            "nutrient": "Phosphorus",
            "fertilizer": "DAP",
            "reason": "Soil phosphorus level is low"
        })

    if soil_k < 40:
        recommendations.append({
            "nutrient": "Potassium",
            "fertilizer": "MOP",
            "reason": "Soil potassium level is low"
        })

    if not recommendations:
        recommendations.append({
            "fertilizer": "NPK 10:26:26",
            "reason": "Soil nutrients are balanced"
        })

    return recommendations
