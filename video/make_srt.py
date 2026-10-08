"""각 곡의 timing.csv로 유튜브 자막 파일(.srt)을 만듭니다.

    python3 make_srt.py      # out/<곡>.srt
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("OUT", os.path.join(HERE, "out"))
SONGS = ["prehistory_song", "samguk_rise_song", "samguk_war_song", "nambukguk_song", "goryeo_early_rap", "goryeo_late_rap", "joseon_early_rap", "joseon_late_rap", "modern_history_rap"]


def ts(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


os.makedirs(OUT, exist_ok=True)
for song in SONGS:
    if not os.path.exists(os.path.join(HERE, song, "timing.csv")):
        continue
    rows = list(csv.DictReader(open(os.path.join(HERE, song, "timing.csv"), encoding="utf-8-sig")))
    path = os.path.join(OUT, song + ".srt")
    with open(path, "w", encoding="utf-8") as f:
        for i, r in enumerate(rows, 1):
            f.write(f"{i}\n{ts(float(r['start']))} --> {ts(float(r['end']))}\n{r['text']}\n\n")
    print(path, len(rows))
