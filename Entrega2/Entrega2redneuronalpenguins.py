# -*- coding: utf-8 -*-
"""RedNeuronalPenguins.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1UTCe0BhBqJv1AmRkhPXf9BQ-4MVSE76q
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
import seaborn as sns
import matplotlib.pyplot as plt

# Sample data structure based on your description
# Load your data here (this is just a representation)
data = pd.read_csv('BillFlipperfinal.csv')

# Step 1: Preprocessing
# Encode species (target variable)
label_encoder_species = LabelEncoder()
data['species'] = label_encoder_species.fit_transform(data['species'])

# Features and labels
X = data[['bill_length_mm', 'flipper_length_mm']]  # Features (bill length and flipper length)
y = data['species']  # Target (species)

# Standardize/normalize the numeric features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Convert labels to categorical format (one-hot encoding)
y_encoded = to_categorical(y)

# Step 2: Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42)

# Step 3: Build the Neural Network
model = Sequential()

# Input layer and hidden layers
model.add(Dense(16, input_dim=2, activation='relu'))  # Input layer with 2 neurons (bill_length_mm, flipper_length_mm)
model.add(Dense(12, activation='relu'))  # Hidden layer

# Output layer (3 classes for the species)
model.add(Dense(3, activation='softmax'))

# Step 4: Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Step 5: Train the model
model.fit(X_train, y_train, epochs=100, batch_size=10, verbose=1)

# Step 6: Evaluate the model on test data
loss, accuracy = model.evaluate(X_test, y_test, verbose=1)
print(f"Test Loss: {loss}")
print(f"Test Accuracy: {accuracy}")

# Step 7: Predictions on the test set
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)  # Convert one-hot encoded predictions back to class labels
y_true_classes = np.argmax(y_test, axis=1)  # Convert one-hot encoded true labels back to class labels

# Step 8: Confusion Matrix
conf_matrix = confusion_matrix(y_true_classes, y_pred_classes, labels=[0, 1, 2])

# Plot the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=label_encoder_species.classes_, yticklabels=label_encoder_species.classes_)
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')
plt.show()

# Step 9: Classification report (Precision, Recall, F1-Score)
print("Classification Report:")
print(classification_report(y_true_classes, y_pred_classes, target_names=label_encoder_species.classes_, labels=[0, 1, 2]))

# Step 10: Accuracy score
print(f"Accuracy Score: {accuracy_score(y_true_classes, y_pred_classes)}")
