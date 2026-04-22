import numpy as np
import pandas as pd
import pickle
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

# ================= LOAD MODEL =================
model = tf.keras.models.load_model("model/deep_model.h5")

with open("model/label_encoder.pkl", "rb") as f:
    le = pickle.load(f)

# Load columns dynamically from dataset if possible
try:
    df_temp = pd.read_csv("data/symptoms_dataset.csv")
    columns = list(df_temp.columns[:-1])
except:
    columns = [
        "weight_loss","fatigue","lump","pain","bleeding",
        "chest_pain","shortness_of_breath","sweating","nausea","arm_pain",
        "weakness","confusion","trouble_speaking","dizziness","headache",
        "memory_loss","difficulty_thinking","mood_changes",
        "swelling","frequent_urination"
    ]

def predict_disease(symptoms):
    input_df = pd.DataFrame([symptoms], columns=columns)

    probs = model.predict(input_df, verbose=0)[0]

    result = {}
    for i, prob in enumerate(probs):
        disease = le.inverse_transform([i])[0]
        result[disease] = round(float(prob * 100), 2)

    return result
