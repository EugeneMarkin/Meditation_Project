from logic.input import InputFile, SoundCollection
from logic.output import OutputFile
from logic.model import Section

def generate():
    sc = SoundCollection(INPUT_PATH)
    out_file = OutputFile(60 * 3 * SAMPLE_RATE)

    sec_normal = Section(dur = 20.0, files = sc.get_by_keyword("body"), mood = Mood.Normal)
    out_file.add_section(sec_normal, at_time = 0.0)

    sec_relaxed = Section(dur = 20.0, files = sc.get_by_keyword("relax"), mood = Mood.Relaxed)
    out_file.add_section(sec_relaxed, at_time = 20.0)

    sec_uncanny = Section(dur = 30.0, files = sc.get_by_keyword("deep"), mood = Mood.Uncanny)
    out_file.add_section(sec_uncanny, 30.0)

    sec_creepy = Section(dur = 40.0, files = sc.get_by_keyword("relax"), mood = Mood.Creepy)
    out_file.add_section(sec_creepy, 50)

    sec_intense = Section(dur = 40.0, files = sc.get_by_keyword("mind"), mood = Mood.Intense)
    out_file.add_section(sec_intense, 60)

    out_file.save_mp3()
