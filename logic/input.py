import os
import random

import pydub
import librosa
import speech_recognition as sr
from constants import SAMPLE_RATE, FOLDER_PATH
from buffer import Buffer
import numpy as np
import sys

class InputFile:

    def __init__(self, name):
        self.name = name
        self.path = FOLDER_PATH + "/" + self.name
        self.name = os.path.splitext(name)[0]
        self.type = os.path.splitext(name)[1][1:]
        self.wav_path = None
        text_path = FOLDER_PATH + "/text/" + self.name + ".txt"
        if os.path.exists(text_path):
            with open(text_path, mode = 'r') as text_file:
                self.text = text_file.read()
        else:
            self.text = ""
        self.duration = 0
        self.spectral_centroid = None
        self.centroid_mean = None

    def read(self):
        if self.wav_path is not None: return
        if self.type == "mp3":
            self.convert_to_wav()
        data, fs = librosa.load(self.wav_path, sr = SAMPLE_RATE)
        self.buf = Buffer(len(data), data = data)
        self.duration = float(len(data))/SAMPLE_RATE
        self.spectral_centroid = librosa.feature.spectral_centroid(y=data, sr = SAMPLE_RATE)[0]
        self.centroid_mean = float(sum(self.spectral_centroid))/len(self.spectral_centroid)


    def convert_to_wav(self):
        self.wav_path = FOLDER_PATH + "/" + "wav" + "/" + self.name + ".wav"
        sound = pydub.AudioSegment.from_mp3(self.path)
        sound.export(self.wav_path, format = "wav")

    def transcribe(self):
        self.read()
        r = sr.Recognizer()
        with sr.AudioFile(self.wav_path) as source:
            audio = r.record(source)
        try:
            res = r.recognize_google(audio)
            self.text = res
            return res
        except sr.UnknownValueError:
            print("Google could not understand audio")
        except sr.RequestError as e:
            print("Google error; {0}".format(e))

        finally:
            if os.path.exists(self.wav_path):
                os.remove(self.wav_path)

class SoundCollection:

    def __init__(self, path):
        self.path = path
        l = os.listdir(FOLDER_PATH)
        self.sounds = list(map(lambda x: InputFile(x), l))

    def __iter__(self):
        return iter(self.sounds)

    def __len__(self):
        return len(self.sounds)

    def get_random(self, count):
        res = []
        for i in range(0, count - 1):
            index = random.randint(0, len(self.sounds) - 1)
            sound = self.sounds[index]
            sound.read()
            res.append(sound)
        return res

    def get_by_keyword(self, kw, n = None):
        if n == None:
            n = 2**15 # or some other big number
        res = []
        for s in self.sounds:
            if len(res) >= n:
                return res
            if kw in s.text:
                s.read()
                res.append(s)
        return res
