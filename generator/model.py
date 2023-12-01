import numpy as np
import random
from enum import Enum

from constants import SAMPLE_RATE, IN_MP3_PATH
from generator.input import InputFile, SoundCollection
from generator.buffer import Buffer, StereoBuffer

class Mood(Enum):
    """
        Mood of a semi-randomly generated audio snippet
        This class also holds the constants for the granulation of the source audio files
        variants: Normal, Relaxed, Uncanny, Creepy, Intense
        The moods are sorted from the less dense granular synthesis params to more dense
    """
    Normal = 0
    Relaxed = 1
    Uncanny = 2
    Creepy = 3
    Intense = 4

    def grain_range(self, file):
        """
        The range of the grain in the source audio file (in samples)
        """
        grain_sizes = [file.duration, file.duration, 3.0, 0.0, 2.0, 1.0]
        grain_sz_var = [0.0, 0.0, 2.0, 3.0, 4.0]
        grain_size = grain_sizes[self.value] + random.uniform(0.0, grain_sz_var[self.value])

        # use 0 size if we want to

        start = int(random.uniform(0, file.duration - grain_size) * SAMPLE_RATE)
        end = int(start + (grain_size * SAMPLE_RATE)) - 1
        return range(start, end)

    def apply_envelope(self, buf):
        sz = len(buf)
        fade_len = int(sz * 0.1)
        attack = np.arange(0, fade_len)/fade_len
        buf.data[0 : fade_len] = buf.data[0 : fade_len] * attack
        release = np.flip(attack)
        buf.data[sz - fade_len : sz] = buf.data[sz - fade_len : sz] * release


    def play_rate(self):
        """
        This mood's play rate, where 1 is the original audio speed
        """
        if self.value <=1:
            return 1
        else:
            return random.choice([1.05, 0.95, 0.9, 0.87, 1.1])

    def density(self) -> int:
        """
        Density of the granulator in grains per seconds
        """
        densities = [0.5, 0.5, 0.6, 1, 2]
        return densities[self.value]

    def amp(self):
        """
        Multiply the source signals to this value
        """
        amps = [0.91, 0.8, 0.9, 0.9, 1.0]
        return amps[self.value]

    def pan(self):
        """
        The position of generated grains in the stereo field: 0 to 1
        """
        if self.value <=1:
            return random.uniform(0.3, 0.7)
        else:
            return random.uniform(0.0, 1.0)

class Section:
    """
    A section is a semi-ramdomly generated snippet of audio
    """
    def __init__(self, dur, files, mood):
        """
        dur - the desired length of the snippet in seconds
        files - a list of source files of type InputFile, from which the snippet is generated
        mood - Normal, Relaxed, Uncanny , Creepy , Intense
        """
        self.dur = dur
        self.buf = StereoBuffer(dur * SAMPLE_RATE)
        self.mood = mood
        self._generate(files)

    def _generate(self, files):
        """
            Fills the section's buffer with the generated audio
        """

        # calculate the number of grains that fits the current duration
        n_grains = int(self.dur * self.mood.density())
        pos = 0
        incr = (self.dur / n_grains) / 2
        for i in range(1, n_grains):
            if pos >= len(self.buf):
                break
            # generate grain
            sound = random.choice(files)
            r = self.mood.grain_range(sound)
            grain_buf = sound.buf.slice(r)
            # Apply randomized amp to each grain
            grain_buf = grain_buf * self.mood.amp()
            # Apply play rate
            grain_buf.play_rate = self.mood.play_rate()
            # Apply envelope
            self.mood.apply_envelope(grain_buf)
            # Add the grain to the final buffer
            pos = random.randint(pos, pos + len(grain_buf))
            self.buf.write(grain_buf, pan_ = self.mood.pan(), at = pos)
            pos += len(grain_buf)


#if __name__ == "__main__":
    #generate()
