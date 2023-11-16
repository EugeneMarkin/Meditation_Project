import os

import wave
from constants import FOLDER_PATH, SAMPLE_RATE
from output import OutputFile
from input import SoundCollection
from buffer import Buffer


def transcribe_all():

    sc = SoundCollection(FOLDER_PATH)
    for s in sc.sounds:
        print("file: ", s.name, "\n")
        try:
            path = FOLDER_PATH + "/text/" + s.name + ".txt"
            if os.path.exists(path):
                 continue
            res = s.transcribe()
            print(res)
            if res == None:
                 continue
            with open(path, mode = "w") as f:
                f.write(res)
        except:
            continue
    return sc


if __name__ == "__main__":
    sc = transcribe_all()
    if sc:
        print("wtf")



# input args

#2. Timeframe (resolution) 10s-30s-50s
#3. Density
#4. Categories: Leadership, productivity, creativity -> Keywords

#timeframes = [10, 30, 150, 20]

#form: breathing, normal, uncanny, intense, creepy, normal

#keywords = ["breathe", "inhale", "breath", "smile"]
#dur = [1]
#offset = [5]

#effects


#/--------------------------------------------------------/ 10 min
#music /--------------------------------------------------------/ 10 min
