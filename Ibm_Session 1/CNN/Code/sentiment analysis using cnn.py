import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense

# Load your CSV dataset
df = pd.read_csv(r"D:\Python\Neural Network\test.csv")

# Extract text and sentiment columns
texts = df["text"].values
sentiments = df["sentiment"].values

# Convert sentiment labels to binary (0 for negative, 1 for positive)
sentiments_binary = np.where(sentiments == "positive", 1, 0)

# Tokenize the text data
num_words = 10000
tokenizer = Tokenizer(num_words=num_words)
tokenizer.fit_on_texts(texts)
text_sequences = tokenizer.texts_to_sequences(texts)
max_sequence_length = max(map(len, text_sequences))
text_sequences_padded = pad_sequences(text_sequences, maxlen=max_sequence_length)

# Create the CNN model
embedding_dim = 128
filters = 64
kernel_size = 3

model_cnn = Sequential([
    Embedding(input_dim=num_words, output_dim=embedding_dim, input_length=max_sequence_length),
    Conv1D(filters=filters, kernel_size=kernel_size, activation='relu'),
    GlobalMaxPooling1D(),
    Dense(units=64, activation='relu'),
    Dense(units=1, activation='sigmoid')
])

model_cnn.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the CNN model
batch_size = 64
epochs = 5
model_cnn.fit(text_sequences_padded, sentiments_binary, batch_size=batch_size, epochs=epochs, validation_split=0.2)

# Function to preprocess and predict sentiment
def predict_sentiment_cnn(text):
    text_sequence = tokenizer.texts_to_sequences([text])
    text_sequence = pad_sequences(text_sequence, maxlen=max_sequence_length)
    sentiment_score = model_cnn.predict(text_sequence)[0][0]
    sentiment = "Positive" if sentiment_score > 0.5 else "Negative"
    return sentiment, sentiment_score

# Input a text for sentiment prediction
input_text = "This movie was a complete disaster. Terrible acting, plot, and direction."
sentiment, sentiment_score = predict_sentiment_cnn(input_text)
print(f"Input Text: {input_text}")
print(f"Predicted Sentiment: {sentiment} (Score: {sentiment_score:.4f})")
