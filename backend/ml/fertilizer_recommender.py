class FertilizerRecommender:
    """
    Provides fertilizer and soil amendment recommendations based on NPK and pH values.
    Uses standard agricultural thresholds.
    """
    
    def recommend(self, n, p, k, ph):
        """
        Generate recommendations.
        :param n, p, k: Soil values in mg/kg (or match unit system)
        :param ph: Soil pH
        :return: List of string messages
        """
        recommendations = []
        
        # --- Nitrogen (N) ---
        if n < 50:
            recommendations.append("Detected Low Nitrogen. Consider applying Urea or Ammonium Sulfate to boost leaf growth.")
        elif n > 140:
            recommendations.append("Detected High Nitrogen. Reduce N-based fertilizers to prevent excessive foliage with less fruit.")

        # --- Phosphorus (P) ---
        if p < 20:
            recommendations.append("Detected Low Phosphorus. Recommended: Single Super Phosphate (SSP) or Di-ammonium Phosphate (DAP) for root strength.")
        elif p > 100:
             recommendations.append("Detected High Phosphorus. Avoid P-rich fertilizers; high P can block micronutrient absorption.")

        # --- Potassium (K) ---
        if k < 50:
            recommendations.append("Detected Low Potassium. Recommended: Muriate of Potash (MOP) to improve disease resistance and water retention.")

        # --- pH Amendments ---
        if ph < 5.5:
            recommendations.append("Soil is Acidic (pH < 5.5). Apply Lime (Calcium Carbonate) to neutralize acidity.")
        elif ph > 8.0:
            recommendations.append("Soil is Alkaline (pH > 8.0). Apply Gypsum or iron sulfate to lower pH.")

        # --- General ---
        if not recommendations:
            recommendations.append("Soil nutrient levels appear balanced. Maintain with organic compost.")
        
        return recommendations
