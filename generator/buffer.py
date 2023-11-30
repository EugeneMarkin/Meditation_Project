from constants import SAMPLE_RATE
import numpy as np
import scipy as sp
from copy import copy

class Buffer:

    def __init__(self, size, data = []):
        self.pr = 1
        if data != []:
            self.data = np.array(data)
        else:
            self.data = np.zeros(size)

    def __mul__(self, other):
        if isinstance(other, float):
            res = self.data * other
            return Buffer(len(res), res.tolist())
        elif isinstance(other, Buffer):
            res = self.data * other.data
            return Buffer(len(res), res.tolist())

    def __len__(self):
        return len(self.data)

    def __copy__(self):
        return Buffer(len(self), list(np.copy(self.data)))

    @property
    def play_rate(self):
        return self.sr

    @play_rate.setter
    def play_rate(self, value):
        if value != self.pr:
            self.pr = value
            new_size = int(len(self.data) / value)
            self._resample_to(new_size)

    def _resample_to(self, size):
        new_sig = sp.signal.resample(self.data, size, window = "hann")
        self.data = np.array(new_sig)


    def write(self, buf, at):
        """
        Write contentes of the argument buffer to this buffer
        at - starting postion in samples
        """
        if len(self.data) < len(buf) + at:
            print("Can't write to buffer. Buffer too small")
            return 1
        self.data[at:at + len(buf)] += buf.data
        return 0

    def slice(self, r: range):
        ar = self.data[r.start:r.stop]
        return Buffer(len(ar), data = ar)

class StereoBuffer:

    def __init__(self, size):
        size = int(size)
        self.size = size
        self.left = Buffer(size)
        self.right = Buffer(size)

    def __copy__(self):
        cp = StereoBuffer(self.size)
        cp.left = copy(self.left)
        cp.right = copy(self.right)
        return cp

    def __len__(self):
        return self.size

    def __mul__(self, other):
        if isinstance(other, float):
            self.left = self.left * other
            self.right = self.right * other
        return self

    def write(self, buf: Buffer, pan_: float, at: int):
        """
        Writes the contents of a given mono buffer to this stereo buffer
        using linear panning, where 0 is left and 1 is right
        at - the staring index of the argument buffer in this buffer in samples
        """
        left_sig = copy(buf) * (1-pan_)
        right_sig = buf * pan_
        self.left.write(left_sig, at)
        self.right.write(right_sig, at)

    def write_stereo(self, buf, at: int):
        """
        Writes the contents of the given stereo buffer to this buffer
        """
        self.left.write(buf.left, at)
        self.right.write(buf.right, at)
