'''
Code for prepairing train_list and eval_list
Data : 30-Oct-2023
Date: 23-Nov-2023
'''
import glob, numpy, os, random, soundfile, torch
from scipy import signal

print("hello preparation code")
train_list_mine = "train_list_v2.txt"
train_path_mine = "../../../../../mnt/disk1/data/DeepMine/wav"
train_list_new = "../../train_list_v3.txt"
eval_list_new = "../../eval_list_v1.txt"
my_eval_path = "../../../../../mnt/disk1/users/afshari/save_list/eval_test1.txt"
num_frames_mine  = 200
data_list_mine   = []
data_label_mine = []
unique_spkr = []
lines = open(train_list_mine).read().splitlines()
dictkeys = list(set([x.split()[0] for x in lines]))
dictkeys.sort()
dictkeys = { key : ii for ii, key in enumerate(dictkeys) }
for index, line in enumerate(lines):
    speaker_label = dictkeys[line.split()[0]]
    if speaker_label not in unique_spkr:
        unique_spkr.append(speaker_label)
    #change here for reading from trainlist of deepmine
    file_name     = os.path.join(train_path_mine, line.split()[0], line.split()[1])
            #file_name     = os.path.join(train_path, line.split()[1])
            #file_name     = os.path.join(train_path, line.split()[2])
    data_label_mine.append(speaker_label)
    data_list_mine.append(file_name)

num_spkr_mine = len(data_label_mine)
print(f"Len Speaker = {num_spkr_mine}")
num_unique_spkr = len(unique_spkr)
print(f"Len Unique Speaker = {num_unique_spkr}")

print(f"audio per Speaker = {num_spkr_mine/num_unique_spkr}")

eval_speaker_mine = 0.2 * num_unique_spkr
num_spkr_eval = eval_speaker_mine
lines2 = open(train_list_mine).read().splitlines()
speaker_data = {}
while num_spkr_eval > 0:
    #print(num_spkr_eval)
    #break;
    for index, line in enumerate(lines2):
        speaker_label = dictkeys[line.split()[0]]
    
        if speaker_label not in speaker_data:
            speaker_data[speaker_label] = []
    
        file_name = os.path.join(train_path_mine, line.split()[0], line.split()[1])
        speaker_data[speaker_label].append(file_name)

    num_spkr_eval -= 1 
print("I have made the dictionary finally")

# Convert dictionary to list of key-value pairs
my_list = [(key, value) for key, value in speaker_data.items()]

# Extract keys and values separately
spkr_list, wavs_list = zip(*my_list)
#Find the min len of wavs for speakers
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
#with open('../../../output_test2.txt', 'w') as file:

with open(my_eval_path, 'w') as file:
    print("Opening file... Please wait.")
    max_spkr1 = 10  # Maximum number of spkr1 items
    max_spkr2 = 10  # Maximum number of spkr2 items
    max_wav1 = 5  # Maximum number of wav1 items per spkr1
    max_wav2 = 5  # Maximum number of wav2 items per spkr2
    counter = 0  # Counter variable
    count_1 = 0  # Counter for '1' entries
    count_0 = 0  # Counter for '0' entries
    entries_written = set()  # Set to store unique entries

    for spkr1_counter in range(max_spkr1):
        for spkr2_counter in range(max_spkr2):
            for wav1_item in wavs_list[spkr1_counter][:max_wav1]:
                for wav2_item in wavs_list[spkr2_counter][:max_wav2]:
                    entry = f'{spkr1_counter}-{spkr2_counter}-{wav1_item}-{wav2_item}'
                    if entry not in entries_written:
                        if spkr_list[spkr1_counter] == spkr_list[spkr2_counter]:
                            file.write(f'1 {wav1_item} {wav2_item}\n')
                            print(f'1 {wav1_item} {wav2_item}\n')
                            count_1 += 1
                        else:
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


print(f"Number of Target '1' entries: {count_1}")
print(f"Number of NonTarget '0' entries: {count_0}")
print("I wrote successfulluy in a text file")
'''
counter = 0
with open(my_eval_path, 'w') as file:
    print("Opening file... Please wait.")
    for spkr1_counter in range(10): #range(len(spkr_list)):
        for spkr2_counter in range(10):#range(spkr1_counter + 1, len(spkr_list)):
            for wav1_item in wavs_list[spkr1_counter]:
                for wav2_item in wavs_list[spkr2_counter]:
                    if spkr_list[spkr1_counter] == spkr_list[spkr2_counter]:
                        #file.write(f'1 {wav1_item} {wav2_item}\n')
                        print(f'1 {wav1_item} {wav2_item}\n')
                    else:
                        #file.write(f'0 {wav1_item} {wav2_item}\n')
                        print(f'0 {wav1_item} {wav2_item}\n')
                    counter = counter +1
                #break;
print(f'counter =  {counter} -----------------------------')
print("I wrote successfulluy in a text file")

'''

'''
# Convert dictionary to list of key-value pairs
my_list = [(key, value) for key, value in speaker_data.items()]
for key, value in speaker_data.items():
    print(key, ":", value[0])
    break;
# Extract keys and values separately
spkr_list, wavs_list = zip(*my_list)

# Initialize lists
labels_eval = []
path1_eval = []
path2_eval = []

# Write the list to a text file
with open('../../output_test.txt', 'w') as file:
    print("open file ... please wait")
    for spkr1_counter in range(len(spkr_list)):
        for spkr2_counter in range(spkr1_counter + 1, len(spkr_list)):
            for wav1_counter in range(len(wavs_list[spkr1_counter])):
                for wav2_counter in range(len(wavs_list[spkr2_counter])):
                    if spkr_list[spkr1_counter] == spkr_list[spkr2_counter]:
                        file.write(f'1 {wavs_list[spkr1_counter][wav1_counter]} {wavs_list[spkr2_counter][wav2_counter]}\n')
                    elif spkr_list[spkr1_counter] != spkr_list[spkr2_counter]:
                        file.write(f'0 {wavs_list[spkr1_counter][wav1_counter]} {wavs_list[spkr2_counter][wav2_counter]}\n')
            break;

'''
'''
my_list = [(key, value) for key, value in speaker_data.items()]
# Extract keys and values separately
spkr_list, wavs_list = zip(*my_list)
i =0
labels_eval =[]
path1_eval=[]
path2_eval=[]
# Write the list to a text file
with open('../../output_test.txt', 'w') as file:
    for spkr1_counter in range(0,len(spkr_list)):
        for wav1_counter in range(0,len(wavs_list)) :
            for spkr2_counter in range(spkr1_counter+1,len(spkr_list)):
                for wav2_counter in range(wav1_counter+1,len(wavs_list)):
                    if spkr_list(spkr1_counter) == spkr_list(spkr2_counter):
                        file.write(f'1 {wavs_list(wav1_counter)} {wavs_list(wav2_counter)} \n')
                    elif spkr_list(spkr1_counter) != spkr_list(spkr2_counter):
                        file.write(f'0 {wavs_list(wav1_counter)} {wavs_list(wav2_counter)} \n')

'''
'''my_dict = {'key1': 1, 'key2': 2, 'key3': 3}

# Convert the dictionary to a list of key-value pairs
dict_list = list(my_dict.items())

# Write the list to a text file
with open('../../output_test.txt', 'w') as file:
    for key, value in dict_list:
        file.write(f'{key}: {value}\n')
print("I wrote successfulluy in a text file")'''
