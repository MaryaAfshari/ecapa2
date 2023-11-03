'''
Code for prepairing train_list and eval_list
Data : 30-Oct-2023
'''
import glob, numpy, os, random, soundfile, torch
from scipy import signal

print("hello preparation code")
train_list_mine = "train_list_v2.txt"
train_path_mine = "../../../../../mnt/disk1/data/DeepMine/wav"
train_list_new = "../../train_list_v3.txt"
eval_list_new = "../../eval_list_v1.txt"
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
for key, value in speaker_data.items():
    print(key, ":", value)
    break;

