import pandas as pd
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    print("Loading dataset...")
    # Load the same dataset used by the project
    data = pd.read_csv("data/symptoms_dataset.csv")

    X = data.iloc[:, :-1].values
    y = data.iloc[:, -1].values

    # Encode labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    y_cat = tf.keras.utils.to_categorical(y_encoded)

    # Split dataset into train and test sets (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_cat, test_size=0.2, random_state=42
    )
    
    print("Building model...")
    # Build the same model as in train_model.py
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(128, input_dim=X.shape[1], activation='relu'))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(64, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(y_cat.shape[1], activation='softmax'))

    model.compile(
        loss=tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.2),
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        metrics=['accuracy']
    )

    print("Training model (this will not save over your existing model)...")
    early_stop = EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True)
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=150, batch_size=4, verbose=0, callbacks=[early_stop])
    print("Training complete.\n")

    print("Evaluating model...")
    # Predict on test data
    y_pred_probs = model.predict(X_test, verbose=0)
    
    y_pred_classes = np.argmax(y_pred_probs, axis=1)
    y_true_classes = np.argmax(y_test, axis=1)

    # Calculate metrics
    # Weighted average is used to account for potential label imbalance
    accuracy = accuracy_score(y_true_classes, y_pred_classes)
    precision = precision_score(y_true_classes, y_pred_classes, average='weighted', zero_division=0)
    recall = recall_score(y_true_classes, y_pred_classes, average='weighted', zero_division=0)
    f1 = f1_score(y_true_classes, y_pred_classes, average='weighted', zero_division=0)

    # Print results in the terminal
    print("=======================================")
    print("        MODEL EVALUATION RESULTS       ")
    print("=======================================")
    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print("=======================================\n")

    # Generate Confusion Matrix Visualization
    print("Generating confusion matrix...")
    cm = confusion_matrix(y_true_classes, y_pred_classes)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=le.classes_, 
                yticklabels=le.classes_)
    plt.title('Disease Prediction Model - Confusion Matrix', fontsize=14)
    plt.xlabel('Predicted Disease', fontsize=12)
    plt.ylabel('Actual Disease', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    output_path = "confusion_matrix.png"
    plt.savefig(output_path, dpi=300)
    print(f"✅ Confusion matrix visualization saved to: {os.path.abspath(output_path)}")
    
    # Try displaying if supported
    try:
        plt.show()
    except Exception:
         pass

if __name__ == "__main__":
    main()
