import os
import random

import pydub
import librosa
import speech_recognition as sr
import numpy as np
import sys

from constants import SAMPLE_RATE, IN_MP3_PATH, IN_WAV_PATH, TEXT_PATH
from generator.buffer import Buffer

class InputFile:

    def __init__(self, name):
        self.name = name
        self.path = IN_MP3_PATH + self.name
        self.name = os.path.splitext(name)[0]
        self.type = os.path.splitext(name)[1][1:]
        self.text_path = TEXT_PATH + self.name + ".txt"
        self.wav_path = IN_WAV_PATH + self.name + ".wav"
        if os.path.exists(self.text_path):
            with open(self.text_path, mode = 'r') as text_file:
                self.text = text_file.read()
        else:
            self.text = ""
        self.duration = 0

    def read(self):
        if not os.path.exists(self.wav_path):
            print("Something went wrong. There's no wav file for ", self.name)
        data, fs = librosa.load(self.wav_path, sr = SAMPLE_RATE)
        self.buf = Buffer(len(data), data = data)
        self.duration = float(len(data))/SAMPLE_RATE


    def convert_to_wav(self):
        if os.path.exists(self.wav_path):
            return
        try:
            sound = pydub.AudioSegment.from_mp3(self.path)
            sound.export(self.wav_path, format = "wav")
        except Exception as e:
            print("Couldn't convert file ", self.path, "error: ", e)
        print("file ", self.path, " converted to wav")

    def transcribe(self):
        if os.path.exists(self.text_path):
            return

        self.read()
        r = sr.Recognizer()
        with sr.AudioFile(self.wav_path) as source:
            audio = r.record(source)
        try:
            res = r.recognize_google(audio)
            self.text = res if res != None else ""
        except sr.UnknownValueError:
            print("Google could not understand audio")
            res = ''
        except sr.RequestError as e:
            print("Google error; {0}".format(e))
            res = ''
        with open(self.text_path, mode = "w") as f:
            f.write(res)

        print("transcription written to ", self.text_path)

class SoundCollection:

    def __init__(self):
        l = os.listdir(IN_MP3_PATH)
        l = list(filter(lambda x: ".mp3" in x, l))
        self.sounds = list(map(lambda x: InputFile(x), l))
        self.prepare()

    def __iter__(self):
        return iter(self.sounds)

    def __len__(self):
        return len(self.sounds)

    def prepare(self):
        for s in self.sounds:
            s.convert_to_wav()
            s.transcribe()

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
