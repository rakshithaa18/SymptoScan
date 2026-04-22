import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping

# ================= LOAD DATA =================
data = pd.read_csv("data/symptoms_dataset.csv")

X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

# ================= ENCODE LABELS =================
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# One-hot encoding (IMPORTANT for softmax)
y_cat = tf.keras.utils.to_categorical(y_encoded)

# ================= SPLIT =================
X_train, X_test, y_train, y_test = train_test_split(
    X, y_cat, test_size=0.2, random_state=42
)

# ================= MODEL =================
model = tf.keras.models.Sequential()

model.add(tf.keras.layers.Dense(128, input_dim=X.shape[1], activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(y_cat.shape[1], activation='softmax'))  # 🔥 KEY

model.compile(
    loss=tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.2), # Label smoothing makes probabilities more realistic!
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    metrics=['accuracy']
)

# ================= TRAIN =================
early_stop = EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True)
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=150, batch_size=4, verbose=1, callbacks=[early_stop])

# ================= SAVE =================
model.save("model/deep_model.h5")

# save label encoder too
with open("model/label_encoder.pkl", "wb") as f:
    pickle.dump(le, f)

print("✅ Deep Learning model trained & saved!")