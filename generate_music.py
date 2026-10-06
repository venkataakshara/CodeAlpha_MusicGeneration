import numpy as np
import tensorflow as tf
import pretty_midi

# Load trained model
model = tf.keras.models.load_model("models/music_model.keras")

# Load sequences
data = np.load("models/sequences.npy")

print("Sequences loaded:", data.shape)

# Starting sequence
sequence = data[0].copy()

generated_notes = []

# Generate 100 notes
for i in range(100):

    input_sequence = sequence[:-1]

    input_sequence = np.expand_dims(
        input_sequence,
        axis=0
    )

    prediction = model.predict(
        input_sequence,
        verbose=0
    )[0]

    pitch = int(
        np.clip(
            round(prediction[0]),
            21,
            108
        )
    )

    velocity = int(
        np.clip(
            round(prediction[1]),
            1,
            127
        )
    )

    start_time = float(prediction[2])
    end_time = float(prediction[3])

    if end_time <= start_time:
        end_time = start_time + 0.5

    generated_notes.append(
        (pitch, velocity, start_time, end_time)
    )

    new_note = np.array(
        [pitch, velocity, start_time, end_time],
        dtype=np.float32
    )

    sequence = np.vstack(
        [sequence[1:], new_note]
    )

# Create MIDI file
midi = pretty_midi.PrettyMIDI()

instrument = pretty_midi.Instrument(
    program=0
)

for pitch, velocity, start, end in generated_notes:

    note = pretty_midi.Note(
        velocity=velocity,
        pitch=pitch,
        start=start,
        end=end
    )

    instrument.notes.append(note)

midi.instruments.append(instrument)

# Save generated music
output_file = "models/generated_music.mid"

midi.write(output_file)

print("\nMusic generation completed!")
print("Generated notes:", len(generated_notes))
print("Saved to:", output_file)