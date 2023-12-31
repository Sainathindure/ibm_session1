import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Load the dataset
data = pd.read_csv("MYDATASET.csv")

# Encode the team names using Label Encoding
label_encoder = LabelEncoder()
data['Team'] = label_encoder.fit_transform(data['Team'])

# Split the dataset into training and testing sets
X = data.drop(['Season', 'W'], axis=1)
y_winner = data['Team']

X_train, X_test, y_winner_train, y_winner_test = train_test_split(
    X, y_winner, test_size=0.2, random_state=42)

# Normalize the input features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Build the ANN model
model = keras.Sequential([
    keras.layers.Input(shape=(X_train.shape[1],)),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(len(label_encoder.classes_), activation='softmax')  # Winner prediction
])

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_winner_train.astype('category').cat.codes, epochs=10, batch_size=32)

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_winner_test.astype('category').cat.codes)
print(f"Winner Prediction Loss: {loss}")
print(f"Winner Prediction Accuracy: {accuracy}")

# Make predictions for the next season
next_season_data = data[data['Season'] == 2022].drop(['Season', 'W'], axis=1)
next_season_data = scaler.transform(next_season_data)
winner_pred = model.predict(next_season_data)
predicted_winner = label_encoder.inverse_transform(np.argmax(winner_pred, axis=1))[0]

print(f"Predicted Winner of 2023: {predicted_winner}")
