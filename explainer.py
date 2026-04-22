import numpy as np
import pandas as pd
from predict import model, columns, le

def normalize_disease_name(name):
    """Maps UI disease names to dataset-specific labels."""
    mapping = {
        "heart disease": "heart attack",
    }
    return mapping.get(name.lower(), name)

def get_top_contributors(symptoms_input, predicted_disease, top_n=3):
    """
    Identifies the top N symptoms that contributed most to the prediction.
    Uses the 'Leave-One-Out' (LOO) perturbation approach.
    """
    # Normalize name to match dataset labels
    predicted_disease = normalize_disease_name(predicted_disease)
    
    # 1. Get the original probability for the target disease
    input_df = pd.DataFrame([symptoms_input], columns=columns)
    original_probs = model.predict(input_df, verbose=0)[0]
    
    # Map disease name to its index in label encoder
    try:
        # le.classes_ are the exact strings from the dataset
        classes_lower = [c.lower() for c in le.classes_]
        disease_idx = classes_lower.index(predicted_disease.lower())
        original_prob = original_probs[disease_idx]
    except (ValueError, IndexError):
        return []

    # 2. Identify indices of selected symptoms (value == 1)
    selected_indices = [i for i, val in enumerate(symptoms_input) if val == 1]
    
    if not selected_indices:
        return []

    impacts = []

    # 3. For each selected symptom, temporarily set it to 0 and re-run prediction
    for idx in selected_indices:
        perturbed_input = list(symptoms_input)
        perturbed_input[idx] = 0
        
        perturbed_df = pd.DataFrame([perturbed_input], columns=columns)
        perturbed_probs = model.predict(perturbed_df, verbose=0)[0]
        perturbed_prob = perturbed_probs[disease_idx]
        
        # Impact is how much the probability DROPPED when this symptom was removed
        impact = original_prob - perturbed_prob
        
        # Realism Fix: Only include positive contributors (Impact > 0)
        # This prevents the AI from listing symptoms that actually made the disease LESS likely.
        if impact > 0.0001: 
            impacts.append((columns[idx], impact))

    # 4. Sort by impact DESC and take top N
    impacts.sort(key=lambda x: x[1], reverse=True)
    
    top_symptoms = [symptom for symptom, impact in impacts[:top_n]]
    return top_symptoms
