import os

import wave
from constants import FOLDER_PATH, SAMPLE_RATE
from output import OutputFile
from input import SoundCollection
from buffer import Buffer

def write_ten_files(to: str):
    out_buf_l = Buffer(10 * 60 * SAMPLE_RATE)
    out_buf_r = Buffer(10 * 60 * SAMPLE_RATE)

    sc = SoundCollection(FOLDER_PATH)
    pos = 0
    for i in range(0, 10):
        sound = sc.sounds[i]
        sound.read()
        out_buf_l.write(sound.buf, at = pos)
        out_buf_r.write(sound.buf, at = pos)
        pos += len(sound.buf)
    out_file = OutputFile([out_buf_l, out_buf_r])
    out_file.save("/Users/eugenemarkin/Documents/meditation/output/outfile1.wav")
    print("will return")
    return 0

def collect():
    sc = SoundCollection(FOLDER_PATH)
    with open(FOLDER_PATH + "/text/text.txt", mode = "w") as f:
        i = 1
        for sound in sc.sounds:
            print(sound.name)
            res = sound.transcribe()
            f.write(str(i) + ": " + sound.name + " text: ")
            i+=1
            if res:
                f.write(res + "\n")
                f.write("dur: " + str(sound.duration) + "\n")
                f.write("sc: " + str(sound.centroid_mean) + "\n")
            else:
                f.write("\n")
            print(res)
            print("dur : ", sound.duration)
            print("sc: ", sound.spectral_centroid)
        f.close()
    return sc

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
