"""첫말⑤ 까꿍 안녕"""
import math
from kids.engine import *
from kids.fw_scene import make_song
from kids.fw_chars import baby_cloud, baby, mom, blanket
def _peek(f, x, y, sc, kind, t):
    paste(f, blanket(120), x, y + 160, scale=sc)
    paste(f, baby_cloud(105, "laugh"), x, y - 20, scale=sc)
def _hi(f, x, y, sc, kind, t):
    paste(f, baby(95, "wave", "손", "laugh"), x, y, scale=sc, rot=6 * math.sin(t * 6))
def _kiss(f, x, y, sc, kind, t):
    paste(f, mom(95, "laugh"), x - 120 * sc, y, scale=sc); paste(f, baby_cloud(70, "laugh"), x + 140 * sc, y + 40, scale=sc)
    paste(f, big_text("♥", 110, (255, 120, 150), (255, 255, 255)), x + 20, y - 150 - 20 * math.sin(t * 4))
def _hug(f, x, y, sc, kind, t):
    paste(f, mom(115, "laugh"), x, y, scale=sc); paste(f, baby_cloud(62, "laugh"), x + 40 * sc, y + 70 * sc, scale=sc)
WORDS = {"까꿍": _peek, "안녕": _hi, "빠이빠이": _hi, "뽀뽀": _kiss, "안아": _hug}
setup, draw = make_song("까꿍 안녕", WORDS, {"까꿍": "까꿍!"}, ((255, 225, 235), (255, 246, 250)), (230, 110, 150), hide="blanket")
