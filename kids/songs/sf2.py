"""첫말② 손 발 눈 코 입"""
from kids.engine import *
from kids.fw_scene import make_song
from kids.fw_chars import baby
POSE = {"손": "clap", "발": "stomp", "눈": "eye", "코": "nose", "입": "mouth"}
def _b(kw): return lambda f, x, y, sc, kind, t: paste(f, baby(95, POSE[kw], kw, "laugh" if kw in ("손", "발") else "smile"), x, y - 70, scale=sc * 0.85)
WORDS = {k: _b(k) for k in POSE}
setup, draw = make_song("손 발 눈 코 입", WORDS, {}, ((200, 238, 230), (240, 252, 248)), (60, 150, 140))
