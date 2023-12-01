import os

SAMPLE_RATE = 44100

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

IN_MP3_PATH = ROOT_DIR + "/input/"
IN_WAV_PATH = IN_MP3_PATH + "wav/"
TEXT_PATH = IN_MP3_PATH + "text/"
MUSIC_PATH = ROOT_DIR + "/music/music.wav"
OUT_MP3_PATH = ROOT_DIR + "/output/out.mp3"
OUT_WAV_PATH = ROOT_DIR + "/output/out.wav"

MUSIC_AMP = 0.15
