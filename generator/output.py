import os
import io
import wave
import numpy as np
import scipy as sp
import struct
import librosa
from copy import copy
from pydub import AudioSegment

from constants import SAMPLE_RATE, IN_MP3_PATH, OUT_MP3_PATH, MUSIC_PATH, MUSIC_AMP
from generator.buffer import Buffer, StereoBuffer
from generator.input import SoundCollection
from generator.model import Section


OUT_PATH = "/Users/eugenemarkin/Documents/meditation/output"

def get_out_file():
    sc = SoundCollection(IN_MP3_PATH)
    music, fs = librosa.load(MUSIC_PATH, sr=SAMPLE_RATE, mono=False)
    dur = len(music[0])

    music_buf = StereoBuffer(dur)
    music_buf.left = Buffer(dur, list(music[0])) * MUSIC_AMP
    music_buf.right = Buffer(dur, list(music[1])) * MUSIC_AMP
    sc = SoundCollection(IN_MP3_PATH)
    of = OutputFile(dur, sc)
    of.buf = copy(music_buf)
    return of

class OutputFile :
    def __init__(self, size, sc):
        self.sc = sc
        self.buf = StereoBuffer(size)
        self.length = len(self.buf)

    def add_section(self, section, at_time: float):
        at = int(at_time * SAMPLE_RATE)
        self.buf.write_stereo(section.buf, at)

    def add(self, dur, kw, mood, at_time):
        self.add_section(Section(dur, self.sc.get_by_keyword(kw), mood), at_time)

    def save(self, to: str):
        try:
            with wave.open(to, "wb") as file:
                file.setnchannels(2)
                file.setsampwidth(2)
                file.setframerate(SAMPLE_RATE)
                file.setnframes(np.uint32(self.length*2))


                scaled_left = (self.buf.left.data * (2**15 - 1)).astype(np.int16)
                scaled_right = (self.buf.right.data * (2**15 - 1)).astype(np.int16)

                stack = np.column_stack((scaled_left, scaled_right)).flatten()
                file.writeframes(stack.tobytes())
                #i = 0
                #for samples in zip(self.left, self.right):
                #    for sample in samples:
                #        print("write frames ", sample, " ", i)
                #        sample = np.uint32(sample * (2 ** 15 - 1))
                #        file.writeframes(struct.pack("<h", sample))
                #        i+=1
            file.close()
        except Exception as e:
            print("exception", str(e))

    def save_mp3(self):

        scaled_left = (self.buf.left.data * (2**15 - 1)).astype(np.int16)
        scaled_right = (self.buf.right.data * (2**15 - 1)).astype(np.int16)
        stack = np.column_stack((scaled_left, scaled_right)).flatten()

        # Convert byte frames to an AudioSegment with stereo channels

        audio_segment = AudioSegment(data=stack.tobytes(), sample_width=2, frame_rate=SAMPLE_RATE, channels=2)


        # Export the AudioSegment to an MP3 file
        audio_segment.export(OUT_MP3_PATH, format='mp3')
