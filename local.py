import sys

from generator.input import SoundCollection
from generator.output import OutputFile
from generator.model import Section, Mood


def generate():
    '''
    An example function to locally generate a meditation file
    '''
    out = OutputFile()

    out.add(dur=30.0, kw="body", mood=Mood.Normal, at_time=0.0)
    out.add(dur=30.0, kw="relax", mood=Mood.Relaxed, at_time=30.0)
    out.add(dur=60.0, kw="body", mood=Mood.Uncanny, at_time=60.0)
    out.add(dur=60.0, kw="relax", mood=Mood.Creepy, at_time=120.0)
    out.add(dur=60.0, kw="mind", mood=Mood.Intense, at_time=180.0)

    out.save_wav()

def prepare():
    '''
    converts all input files to wav and transcribes them to text,
    so that they can be used in audio generation
    '''
    sc = SoundCollection()
    sc.prepare()

if __name__ == "__main__":
    argument = sys.argv[1]
    print("arg ", argument)
    if argument == 'prepare':
        prepare()
    elif argument == 'generate':
        generate()
    else:
        print("unknown argument")
