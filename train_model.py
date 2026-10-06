import numpy as np
import tensorflow as tf

Sequential = tf.keras.models.Sequential
LSTM = tf.keras.layers.LSTM
Dense = tf.keras.layers.Dense
Adam = tf.keras.optimizers.Adam

# Load sequences
data = np.load("models/sequences.npy")

print("Data shape:", data.shape)

# Use a smaller dataset for the first training test
max_sequences = 50000

if len(data) > max_sequences:
    data = data[:max_sequences]

print("Training sequences:", len(data))

# Input and output
X = data[:, :-1, :]
y = data[:, -1, :]

print("X shape:", X.shape)
print("y shape:", y.shape)

# Build LSTM model
model = Sequential()

model.add(
    LSTM(
        128,
        input_shape=(X.shape[1], X.shape[2])
    )
)

model.add(Dense(64, activation="relu"))
model.add(Dense(4))

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss="mse"
)

model.summary()

# Train
model.fit(
    X,
    y,
    epochs=10,
    batch_size=64,
    validation_split=0.1
)

# Save model
model.save("models/music_model.keras")

print("Model training completed!")
print("Model saved to: models/music_model.keras")