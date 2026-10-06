import os
import pretty_midi
import pickle

dataset_path = "dataset"
output_file = "models/notes.pkl"

all_notes = []

midi_files = []

for root, dirs, files in os.walk(dataset_path):
    for file in files:
        if file.endswith(".mid") or file.endswith(".midi"):
            midi_files.append(os.path.join(root, file))

print("Total MIDI files:", len(midi_files))

for index, file_path in enumerate(midi_files):

    try:
        midi = pretty_midi.PrettyMIDI(file_path)

        for instrument in midi.instruments:

            for note in instrument.notes:

                note_data = (
                    note.pitch,
                    note.velocity,
                    round(note.start, 3),
                    round(note.end, 3)
                )

                all_notes.append(note_data)

        if (index + 1) % 100 == 0:
            print("Processed:", index + 1)

    except Exception as e:
        print("Error:", file_path)
        print(e)

os.makedirs("models", exist_ok=True)

with open(output_file, "wb") as file:
    pickle.dump(all_notes, file)

print("\nDataset preparation completed!")
print("Total notes extracted:", len(all_notes))
print("Saved to:", output_file)