import os
import wave
import numpy as np
import scipy as sp
import struct
from constants import SAMPLE_RATE, OUT_MP3_PATH
from buffer import Buffer, StereoBuffer


OUT_PATH = "/Users/eugenemarkin/Documents/meditation/output"


class OutputFile :
    def __init__(self, size: int):
        self.buf = StereoBuffer(size)
        self.length = len(self.buf)

    def add_section(self, section, at_time: float):
        at = int(at_time * SAMPLE_RATE)
        self.buf.write_stereo(section.buf, at)


    def save(self, to: str):
        try:
            with wave.open(to, "wb") as file:
                file.setnchannels(2)
                file.setsampwidth(2)
                file.setframerate(SAMPLE_RATE)
                file.setnframes(np.uint32(self.length*2))

                print("slef buf is ", self.buf)
                print("left ", self.buf.left)
                print("right ", self.buf.right)

                scaled_left = (self.buf.left.data * (2**15 - 1)).astype(np.int16)
                scaled_right = (self.buf.right.data * (2**15 - 1)).astype(np.int16)

                stack = np.column_stack((scaled_left, scaled_right)).flatten()
                print("scaled_left", scaled_left[1:10])
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
