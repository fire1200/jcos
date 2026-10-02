"""모음 영상 썸네일. 사용: python -m kids.compile_thumb out.jpg "윗줄" "아랫줄" "13분"""
import sys
from kids.engine import *
from kids.brand import badge

def make(out, a, b, length):
    f = vgrad((150, 210, 250), (235, 247, 255))
    hills(f, 860, (180, 228, 160), 30, 1.6)
    paste(f, rainbow(520, 22), 960, 700)
    paste(f, dino(120, 2, "laugh"), 420, 700)
    paste(f, squirrel(110, "laugh", 0.6), 1530, 690)
    paste(f, bubble(130), 1600, 300); paste(f, cloud_char(48, "laugh"), 1600, 310)
    paste(f, cloud_char(120, "laugh"), 330, 260)
    paste(f, cloud_char(70, "o", (255, 205, 225)), 960, 250)
    paste(f, big_text(a, 150, (255, 255, 255), (95, 140, 225)), 960, 520)
    paste(f, big_text(b, 170, (255, 240, 120), (95, 140, 225)), 960, 700)
    paste(f, badge(length, (95, 140, 225)), 1740, 980)
    paste(f, badge("창작동요"), 180, 70)
    f.convert("RGB").resize((1280, 720), Image.LANCZOS).save(out, quality=92)

if __name__ == "__main__":
    make(*sys.argv[1:5])
