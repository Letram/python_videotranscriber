import sys
import getopt
import math
import time
from os import path as path
import os
from pydub import AudioSegment


class SplitWavAudioMubin():
    """
    def __init__(self, folder, filename):
        self.folder = folder
        self.filename = filename
        self.filepath = folder + '\\' + filename
        self.audio = AudioSegment.from_wav(self.filepath)

    def __init__(self, file, filename, folder):
        super().__init__()
        self.file = file
        self.filename = filename
        self.folder = folder
        self.audio = AudioSegment.from_wav(self.file)
    """

    def __init__(self):
        super().__init__()

    def get_duration(self):
        return self.audio.duration_seconds

    def single_split(self, from_min, to_min, split_filename):
        t1 = from_min * 60 * 1000
        t2 = to_min * 60 * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export(self.folder + split_filename + ".wav", format="wav")

    def single_split_sec(self, from_sec, to_sec, split_filename, to_file):
        t1 = from_sec * 1000
        t2 = to_sec * 1000
        time_1 = time.strftime("%H:%M:%S", time.gmtime(from_sec))
        time_2 = time.strftime("%H:%M:%S", time.gmtime(to_sec))
        split_audio = self.audio[t1:t2]
        if(to_file):
            split_audio.export(
                self.folder + "/" + split_filename + ".wav", format="wav")

        return {
            "from_time": time_1,
            "to_time": time_2,
            "duration": split_audio.duration_seconds,
            "audio_path": self.folder + "/" + split_filename + ".wav"
        }

    def multiple_split(self, min_per_split):
        total_mins = math.ceil(self.get_duration() / 60)
        for i in range(0, total_mins, min_per_split):
            split_fn = str(i) + '_' + self.filename
            self.single_split(i, i+min_per_split, split_fn)
            #print(str(i) + ' Done')
            if i == total_mins - min_per_split:
                print('All splitted successfully')

    def multiple_split_seconds(self, audio_path, folder_path, to_file, sec_per_split):
        self.audio = AudioSegment.from_wav(audio_path)
        self.folder = folder_path

        total_secs = math.ceil(self.get_duration())
        audio_segments = []

        filename = path.splitext(path.basename(audio_path))[0]
        for i in range(0, total_secs, sec_per_split):
            split_fn = "{0}_".format(filename) + \
                "{:05d}".format(int(i/sec_per_split))
            segment = self.single_split_sec(
                i, i+sec_per_split, split_fn, to_file)
            audio_segments.append(segment)
            #print(str(i) + ' Done')
            if i == total_secs - sec_per_split:
                print('All splited successfully')
        return audio_segments


"""
    def multiple_split_seconds(self, sec_per_split, to_file = True):
        total_secs = math.ceil(self.get_duration())
        audio_segments = []
        for i in range(0, total_secs, sec_per_split):
            split_fn =  "{0}_".format(self.filename) + "{:05d}".format(int(i/sec_per_split))
            segment = self.single_split_sec(i, i+sec_per_split, split_fn, to_file)
            audio_segments.append(segment)
            print(str(i) + ' Done')
            if i == total_secs - sec_per_split:
                print('All splited successfully')
        return audio_segments
 """


def main(argv):
    sound = ""
    folder = ""
    filename = ""
    block_of_seconds = 20
    try:
        opts = getopt.getopt(argv, "s:f:n:t:", ["src="])

    except getopt.GetoptError:
        print('splitter.py -s <audiosource> -f <foldername> -n <filename> (optional) -t <blockofseconds>')
        sys.exit(2)

    # Este for recorre cada una de las opciones que le pasamos al script como clave-valor (option, argument)
    for opt, arg in opts:
        if opt == "-h":
            print('splitter.py -s <audiosource> -f <foldernametosave> -n <filenametosave> (optional) -t <blockofseconds>')
        elif opt in ("-s", "--soundfile"):
            sound = arg
        elif opt in ("-f", "--folder"):
            folder = arg
        elif opt in ("-n", "--filename"):
            filename = arg
        elif opt in ("-t", "--time"):
            block_of_seconds = arg

    split_wav = SplitWavAudioMubin(sound, filename, folder)
    # split_wav.multiple_split(min_per_split=1)
    # audio_segments = split_wav.multiple_split_seconds(sec_per_split=block_of_seconds)


def split(audio_path, folder_path, block_of_seconds, to_file):
    splitter = SplitWavAudioMubin()
    if os.path.isdir(folder_path):
        for f in os.listdir(folder_path):
            os.remove(folder_path + "/" + f)
    return splitter.multiple_split_seconds(audio_path, folder_path, to_file, block_of_seconds)


if __name__ == "__main__":
    main(sys.argv[1:])
