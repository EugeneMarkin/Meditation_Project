from generator.input import InputFile
from generator.output import OutputFile
from generator.model import Section, Mood

async def generate():
    out = OutputFile()

    out.add(dur=30.0, kw="body", mood=Mood.Normal, at_time=0.0)
    out.add(dur=30.0, kw="relax", mood=Mood.Relaxed, at_time=30.0)
    out.add(dur=60.0, kw="body", mood=Mood.Uncanny, at_time=60.0)
    out.add(dur=60.0, kw="relax", mood=Mood.Creepy, at_time=120.0)
    out.add(dur=60.0, kw="mind", mood=Mood.Intense, at_time=180.0)

    out.save_wav()
