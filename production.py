from generator.input import InputFile, SoundCollection
from generator.output import get_out_file
from generator.model import Section, Mood

def generate():
    out = get_out_file()

    out.add(dur=30.0, kw="body", mood=Mood.Normal, at_time=0.0)
    out.add(dur=30.0, kw="relax", mood=Mood.Relaxed, at_time=30.0)
    out.add(dur=60.0, kw="body", mood=Mood.Uncanny, at_time=60.0)
    out.add(dur=60.0, kw="relax", mood=Mood.Creepy, at_time=120.0)
    out.add(dur=60.0, kw="mind", mood=Mood.Intense, at_time=180.0)

    out.save_mp3()

    out_file.save_mp3()
