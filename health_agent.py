def get_health_recommendation(disease_name, probability):
    """
    AI Health Assistant Agent.
    Generates simple medical guidance based on the predicted disease and probability.
    """
    disease_name = disease_name.lower()
    
    # Low Risk Condition
    if probability < 30:
        return "The predicted risk is low according to our model. However, if your symptoms persist or worsen, a routine medical check-up is advisable."
    
    is_high_risk = probability >= 70

    if "cancer" in disease_name:
        return "We strongly suggest scheduling a consultation with an oncologist for detailed evaluation."
    elif "tuberculosis" in disease_name.lower() or "tb" in disease_name:
        return "We suggest visiting a pulmonologist and getting a formal TB test (e.g., chest X-ray or sputum test)."
    elif "stroke" in disease_name:
        if is_high_risk:
            return "⚠️ CRITICAL: Seek urgent medical attention immediately or call emergency services! Time is highly critical for stroke diagnosis."
        else:
            return "Moderate risk of stroke detected. Please seek medical consultation promptly to rule out serious conditions."
    elif "alzheimer" in disease_name:
        return "We suggest arranging a neurological consultation and a cognitive evaluation for comprehensive care planning."
    elif "heart" in disease_name:
        if is_high_risk:
            return "⚠️ CRITICAL: High risk of heart disease! Please consult a cardiologist immediately or seek urgent care if experiencing severe chest pain."
        else:
            return "It is recommended to consult a cardiologist promptly for a proper cardiovascular assessment."
    else:
        return "Please consult a healthcare professional or specialist for an accurate diagnosis and treatment plan."
