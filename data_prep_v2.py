import os
import random
import glob, numpy, os, random, soundfile, torch
from scipy import signal

train_list_mine = "train_list_mine.txt"
train_list_new = "train_list_new.txt"
train_path_mine = "/path/to/train_data"

# Read train_list_mine file
lines = open(train_list_mine).read().splitlines()

# Get unique speakers from train_list_mine
unique_spkr = list(set([line.split()[0] for line in lines]))
num_unique_spkr = len(unique_spkr)

# Calculate the number of speakers to keep (80% of unique speakers)
num_spkr_keep = int(0.8 * num_unique_spkr)

# Randomly select the speakers to keep
random.seed(42)  # Set the random seed for reproducibility
speakers_to_keep = random.sample(unique_spkr, num_spkr_keep)

# Create train_list_new file with lines related to the selected speakers
with open(train_list_new, 'w') as f:
    for line in lines:
        speaker_label = line.split()[0]
        if speaker_label in speakers_to_keep:
            f.write(line + '\n')

# Create speaker_data dictionary for remaining speakers
speaker_data = {}
for line in lines:
    speaker_label = line.split()[0]
    if speaker_label not in speakers_to_keep:
        if speaker_label not in speaker_data:
            speaker_data[speaker_label] = []
        file_name = os.path.join(train_path_mine, line.split()[0], line.split()[1])
        speaker_data[speaker_label].append(file_name)

print("Train list files created and speaker_data dictionary created.")