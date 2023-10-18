'''
DataLoader for training
'''
# def __init__(self, train_list, train_path, musan_path, rir_path, num_frames, **kwargs):
import glob, numpy, os, random, soundfile, torch
from scipy import signal

class train_loader(object):
    def __init__(self, train_list, train_path, num_frames, **kwargs):
        self.train_path = train_path
        self.num_frames = num_frames
        self.data_list  = []
        self.data_label = []
        lines = open(train_list).read().splitlines()
        dictkeys = list(set([x.split()[0] for x in lines]))
        dictkeys.sort()
        dictkeys = { key : ii for ii, key in enumerate(dictkeys) }
        for index, line in enumerate(lines):

            speaker_label = dictkeys[line.split()[0]]
            #change here for reading from trainlist of deepmine
            file_name     = os.path.join(train_path, line.split()[0], line.split()[1])
            #file_name     = os.path.join(train_path, line.split()[1])
            #file_name     = os.path.join(train_path, line.split()[2])
            self.data_label.append(speaker_label)
            self.data_list.append(file_name)

    def __getitem__(self, index):
        # Read the utterance and randomly select the segment
        audio, sr = soundfile.read(self.data_list[index])
        #print("Audio shape:", audio.shape)		
        length = self.num_frames * 160 + 240
        if audio.shape[0] <= length:
            shortage = length - audio.shape[0]
            audio = numpy.pad(audio, (0, shortage), 'wrap')
        start_frame = numpy.int64(random.random()*(audio.shape[0]-length))
        audio = audio[start_frame:start_frame + length]
        return torch.FloatTensor(numpy.array(audio)), self.data_label[index]
        

    def __len__(self):
        return len(self.data_list)
