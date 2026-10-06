import os

dataset_path = "dataset"

count = 0

for root, folders, files in os.walk(dataset_path):

    for file in files:

        if file.endswith(".midi") or file.endswith(".mid"):

            count += 1

            if count <= 10:
                print(file)

print("\nTotal MIDI files found:", count)