from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import pandas as pd

# ✅ IMPORT PREDICT FUNCTION
from predict import predict_disease
from health_agent import get_health_recommendation
from explainer import get_top_contributors

app = Flask(__name__)
CORS(app)

# ================= MONGODB =================
client = MongoClient("mongodb://localhost:27017/")
db = client["symptoscan"]

users_collection = db["users"]
history_collection = db["history"]

# ================= ROUTES =================
from flask import request, jsonify
from groq import Groq

client = Groq(api_key="xx")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    symptoms = data.get("symptoms", [])
    disease = data.get("disease", "")

    try:
        prompt = f"""
You are a helpful AI health assistant.

User has selected these symptoms:
{", ".join(symptoms)}

Predicted disease:
{disease}

User question:
{user_msg}

Instructions:
- Do NOT ask for symptoms again
- Use given symptoms to answer
- Give general advice only
- Keep it short
- Suggest doctor if needed
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # 🔥 powerful model
            messages=[
                {"role": "system", "content": "You are a medical assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        reply = response.choices[0].message.content

        return jsonify({"reply": reply})

    except Exception as e:
        print("Groq Error:", e)
        return jsonify({"reply": str(e)})
    
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# 🔥 UPDATED (force fresh load)
@app.route("/history")
def history_page():
    return render_template("history.html")


# ================= REGISTER =================
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'GET':
        return render_template("register.html")

    if request.is_json:
        data = request.get_json()

        if users_collection.find_one({"email": data["email"]}):
            return jsonify({"message": "User already exists"})

        users_collection.insert_one({
            "username": data["username"],
            "email": data["email"],
            "phone": data["phone"],
            "password": data["password"]
        })

        return jsonify({"message": "Registered successfully"})

    return jsonify({"error": "Invalid request"}), 400


# ================= LOGIN =================
@app.route('/login', methods=['POST'])
def login():
    data = request.json

    user = users_collection.find_one({
        "email": data["email"],
        "password": data["password"]
    })

    if user:
        return jsonify({"message": "Login success"})
    else:
        return jsonify({"message": "Invalid credentials"}), 401


# ================= PREDICT =================
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        symptoms = data["symptoms"]
        email = data.get("email")

        predictions = predict_disease(symptoms)

        clean_predictions = {
            k: float(v) for k, v in predictions.items()
        }

        top_disease = max(clean_predictions, key=clean_predictions.get)
        top_prob = clean_predictions[top_disease]

        history_collection.insert_one({
            "email": email,
            "symptoms": symptoms,
            "predictions": clean_predictions,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "prediction": top_disease,
            "probability": top_prob
        })

        recommendation = get_health_recommendation(top_disease, top_prob)

        target = data.get("target_disease", top_disease)
        explanation = get_top_contributors(symptoms, target)

        return jsonify({
            "predictions": clean_predictions,
            "top_disease": top_disease,
            "top_probability": top_prob,
            "recommendation": recommendation,
            "explanation": explanation,
            "explanation_target": target
        })

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"error": str(e)}), 500


# ================= GET USER =================
@app.route('/get-user/<email>')
def get_user(email):
    user = users_collection.find_one({"email": email}, {"_id": 0})
    return jsonify(user)


# ================= GET HISTORY =================
@app.route('/history/<email>', methods=['GET'])
def get_history(email):
    records = list(history_collection.find({"email": email}, {"_id": 0}))
    return jsonify(records)


# ================= GET SYMPTOMS =================
@app.route('/api/symptoms', methods=['GET'])
def get_symptoms():
    try:
        df = pd.read_csv("data/symptoms_dataset.csv")
        symptoms = list(df.columns[:-1])
        return jsonify(symptoms)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= MODEL PERFORMANCE =================
@app.route('/model_performance', methods=['GET'])
def model_performance():
    return jsonify({
        "accuracy": 0.96,
        "precision": 0.965,
        "recall": 0.96,
        "f1_score": 0.9607
    })


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)