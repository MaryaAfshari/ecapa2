import os
import random

train_list_mine = "train_list_mine.txt"
train_list_new = "train_list_new.txt"
train_path_mine = "/path/to/train_data"
my_eval_path = "output_test2.txt"


print("hello preparation code")
train_list_mine = "train_list_v2.txt"
train_path_mine = "../../../../../mnt/disk1/data/DeepMine/wav"
train_list_new = "../../../../../mnt/disk1/users/afshari/save_list/train_list_v4.txt"
eval_list_new = "../../../../../mnt/disk1/users/afshari/save_list/eval_list_v4.txt"
my_eval_path = "../../../../../mnt/disk1/users/afshari/save_list/eval_test_v4.txt"
num_frames_mine  = 200

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

print("Train list new is created.")
# Create speaker_data dictionary for remaining speakers
speaker_data = {}
for line in lines:
    speaker_label = line.split()[0]
    if speaker_label not in speakers_to_keep:
        if speaker_label not in speaker_data:
            speaker_data[speaker_label] = []
        file_name = os.path.join(train_path_mine, line.split()[0], line.split()[1])
        speaker_data[speaker_label].append(file_name)

print("Speaker_data dictionary is created.")

# Convert dictionary to list of key-value pairs
my_list = [(key, value) for key, value in speaker_data.items()]

# Extract keys and values separately
spkr_list, wavs_list = zip(*my_list)

# Find the minimum length of wavs for speakers
min_length = float('inf')  # Initialize with a large value

for spkr1_counter in range(len(spkr_list)):
    current_length = len(wavs_list[spkr1_counter])
    if current_length < min_length:
        min_length = current_length

print(f"The minimum number of elements in wav_list is: {min_length}")

# Prompt the user to enter 'y' or 'n' to continue or stop
choice = input("Enter 'y' to continue or 'n' to stop: ")

# Keep prompting until 'y' or 'n' is entered
while choice != 'y' and choice != 'n':
    choice = input("Invalid input. Enter 'y' to continue or 'n' to stop: ")

# Check the choice
if choice == 'y':
    print("Continuing...")
    # Rest of your code goes here
else:
    print("Stopping the program.")
    # Any necessary cleanup or actions to stop the program

# Convert dictionary to list of key-value pairs
my_list = [(key, value) for key, value in speaker_data.items()]

# Extract keys and values separately
spkr_list, wavs_list = zip(*my_list)

# Initialize lists
labels_eval = []
path1_eval = []
path2_eval = []

# Write the list to a text file
with open(my_eval_path, 'w') as file:
    print("Opening file... Please wait.")
    max_spkr1 = 10  # Maximum number of spkr1 items
    max_spkr2 = 10  # Maximum number of spkr2 items
    max_wav1 = 50  # Maximum number of wav1 items per spkr1
    max_wav2 = 50  # Maximum number of wav2 items per spkr2
    counter = 0  # Counter variable
    count_1 = 0  # Counter for '1' entries
    count_0 = 0  # Counter for '0' entries
    entries_written = set()  # Set to store unique entries

    while count_1 < 10000 or count_0 < 15000:
        for spkr1_counter in range(max_spkr1):
            for spkr2_counter in range(max_spkr2):
                for wav1_item in wavs_list[spkr1_counter][:max_wav1]:
                    for wav2_item in wavs_list[spkr2_counter][:max_wav2]:
                        entry = f'{spkr1_counter}-{spkr2_counter}-{wav1_item}-{wav2_item}'
                        if entry not in entries_written:
                            if spkr_list[spkr1_counter] == spkr_list[spkr2_counter]:
                                if count_1 < 10000:
                                    file.write(f'1 {wav1_item} {wav2_item}\n')
                                    print(f'1 {wav1_item} {wav2_item}\n')
                                    count_1 += 1
                            else:
                                if count_0 < 15000:
                                    file.write(f'0 {wav1_item} {wav2_item}\n')
                                    print(f'0 {wav1_item} {wav2_item}\n')
                                    count_0 += 1
                            entries_written.add(entry)
                            counter += 1
                            if counter == (max_spkr1 * max_spkr2 * max_wav1 * max_wav2):
                                break
                    if counter == (max_spkr1 * max_spkr2 * max_wav1 * max_wav2):
                        break
                if counter == (max_spkr1 * max_spkr2 * max_wav1 * max_wav2):
                    break
            if counter == (max_spkr1 * max_spkr2 * max_wav1 * max_wav2):
                break
        if counter == (max_spkr1 * max_spkr2 * max_wav1 * max_wav2):
            break

print(f"Number of '1' entries: {count_1}")
print(f"Number of '0' entries: {count_0}")
print("I wrote successfully in a text file.")