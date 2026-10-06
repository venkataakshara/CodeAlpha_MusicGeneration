import pickle
import numpy as np

input_file = "models/notes.pkl"
output_file = "models/sequences.npy"

with open(input_file, "rb") as file:
    notes = pickle.load(file)

print("Total notes loaded:", len(notes))

sequence_length = 50

sequences = []

for i in range(len(notes) - sequence_length):
    sequence = notes[i:i + sequence_length]
    sequences.append(sequence)

sequences = np.array(sequences, dtype=np.float32)

np.save(output_file, sequences)

print("Sequences created:", len(sequences))
print("Sequence shape:", sequences.shape)
print("Saved to:", output_file)
