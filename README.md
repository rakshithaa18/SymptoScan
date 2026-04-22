# SymptoScan  
AI-Powered Disease Prediction System

SymptoScan is a healthcare assistance system that predicts possible diseases based on user symptoms using a Deep Learning model. It also includes a chat-based AI assistant for user interaction and guidance.

---

## Features

- Disease prediction based on symptoms  
- Probability-based output  
- Deep Learning model (Multilayer Perceptron)  
- AI chat assistant  
- User history storage  
- Simple and user-friendly interface  

---

## How It Works

1. User selects symptoms  
2. Symptoms are converted into a binary vector (0 or 1)  
3. The vector is passed to a neural network model  
4. The model predicts the disease and probability  
5. The result is displayed and stored in the database  

---

## Tech Stack

Frontend:
- HTML  
- CSS  
- JavaScript  

Backend:
- Flask (Python)  

Database:
- MongoDB  

Machine Learning:
- TensorFlow / Keras  
- Multilayer Perceptron (MLP)  

---

## Model Details

- Input: 20 symptoms  
- Hidden Layers: Dense layers with ReLU activation  
- Output Layer: Softmax activation (multi-class classification)  

---
