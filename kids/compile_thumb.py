"""모음 영상 썸네일. 사용: python -m kids.compile_thumb out.jpg "윗줄" "아랫줄" "13분" [그림 1|2|3|4]"""
import sys
from kids.engine import *
from kids.brand import badge

def make(out, a, b, length, art="1"):
    if art == "3":  # 모음03 잠자리: 밤하늘, 달, 별 요정, 곰 인형, 그림자 친구
        f = vgrad((24, 30, 78), (88, 80, 150))
        for i in range(45):
            paste(f, star(5 + i % 5, (255, 236, 170)), (i * 397) % W, (i * 211) % 640 + 20, alpha=0.5 + 0.1 * (i % 5))
        hills(f, 880, (110, 100, 170), 25, 1.4)
        paste(f, moon(150), 1600, 260)
        paste(f, fairy(80, "smile"), 330, 280)
        paste(f, bear(120, "smile"), 380, 760)
        paste(f, cub(110, "smile"), 1560, 760)
        paste(f, big_text(a, 150, (255, 255, 255), (70, 70, 140)), 960, 520)
        paste(f, big_text(b, 170, (255, 240, 120), (70, 70, 140)), 960, 700)
        paste(f, badge(length, (70, 70, 140)), 1740, 980)
        paste(f, badge("창작동요"), 180, 70)
        f.convert("RGB").resize((1280, 720), Image.LANCZOS).save(out, quality=92); return
    f = vgrad((150, 210, 250), (235, 247, 255))
    hills(f, 860, (180, 228, 160), 30, 1.6)
    if art == "4":  # 모음04 전곡: 해와 달, 친구들 모두
        paste(f, rainbow(560, 24), 960, 760)
        paste(f, sun(80), 330, 220); paste(f, moon(70), 1600, 220)
        for x, sp in [(200, dino(90, 1, "laugh")), (420, sock(90, "laugh")), (1500, squirrel(85, "laugh", 0.6)), (1720, bunny(85, "laugh"))]:
            paste(f, sp, x, 790)
        paste(f, fairy(50, "laugh"), 960, 240)
        paste(f, cloud_char(70, "laugh"), 760, 230); paste(f, cloud_char(60, "laugh", (255, 215, 230)), 1160, 250)
    elif art == "2":  # 모음02: 무지개 크게, 양말·고래·공룡
        paste(f, rainbow(640, 30), 960, 760)
        paste(f, sock(130, "laugh"), 380, 720, rot=-10)
        paste(f, sock(110, "laugh", (110, 160, 235)), 520, 760, rot=8)
        paste(f, dino(110, 1, "laugh"), 1560, 710)
        paste(f, bubble(120), 330, 280); paste(f, cloud_char(44, "laugh"), 330, 290)
        paste(f, cloud_char(110, "laugh", (255, 215, 230)), 1600, 260)
        paste(f, cloud_char(70, "laugh"), 960, 240)
    else:
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
    make(*sys.argv[1:6])
