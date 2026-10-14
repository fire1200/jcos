"""첫말⑥ 자자 코~ (잠자리)"""
import math
from kids.engine import *
from kids.fw_scene import make_song
from kids.fw_chars import blanket, pillow, baby_cloud
STARS = [((i * 397) % W, (i * 211) % 600 + 30, 5 + i % 4) for i in range(36)]
def bg(t):
    f = vgrad((30, 34, 80), (80, 76, 140))
    for i, (x, y, r) in enumerate(STARS):
        paste(f, star(r, (255, 236, 170)), x, y, alpha=0.4 + 0.3 * (0.5 + 0.5 * math.sin(t * 1.5 + i)))
    hills(f, 900, (95, 90, 150), 20, 1.3)
    return f
def _blanket(f, x, y, sc, kind, t):
    paste(f, baby_cloud(80, "squint"), x, y - 70, scale=sc); paste(f, blanket(120), x, y + 50, scale=sc)
def _pillow(f, x, y, sc, kind, t):
    paste(f, pillow(120), x, y + 40, scale=sc); paste(f, baby_cloud(70, "smile"), x, y - 60, scale=sc)
def _moon(f, x, y, sc, kind, t): paste(f, moon(130, face_kind="smile"), x, y, scale=sc)
def _star(f, x, y, sc, kind, t): paste(f, star(120, (255, 225, 120), "smile"), x, y, scale=sc, rot=8 * math.sin(t * 2))
def _sleep(f, x, y, sc, kind, t):
    paste(f, pillow(110), x, y + 20, scale=sc); paste(f, baby_cloud(75, "squint"), x, y - 40 + 6 * math.sin(t * 1.5), scale=sc)
    paste(f, blanket(110), x, y + 110, scale=sc)
    for k in range(3):
        q = (t * 0.4 + k / 3) % 1; paste(f, big_text("z", 50 + 20 * k, (255, 255, 255), (90, 90, 160)), x + 180 + 60 * q, y - 120 - 140 * q, alpha=1 - q)
WORDS = {"이불": _blanket, "베개": _pillow, "달": _moon, "별": _star, "자자": _sleep, "코~": _sleep}
setup, draw = make_song("자자 코~", WORDS, {"코~": "코~", "자자": "자자"}, bg, (90, 90, 170), hide="blanket", cap_fg=(90, 90, 170), night=True)
