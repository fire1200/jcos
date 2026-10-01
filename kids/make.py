"""사용: python -m kids.make NN audio.mp3 lines.json out.mp4 [--preview t1,t2,...]"""
import sys, json, importlib, subprocess, os
from kids import engine

def duration(path):
    out = subprocess.run([engine.FFMPEG, "-i", path], capture_output=True, text=True).stderr
    import re
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", out).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)

if __name__ == "__main__":
    n, audio, lines, out = sys.argv[1:5]
    prev = [float(x) for x in sys.argv[6].split(",")] if len(sys.argv) > 6 and sys.argv[5] == "--preview" else None
    mod = importlib.import_module(f"kids.songs.s{n}")
    total = duration(audio)
    ctx = mod.setup(json.load(open(lines)), total)
    engine.render(mod.draw, audio, out, total, ctx, preview=prev, fade=getattr(mod, "FADE_OUT", 2.5))
