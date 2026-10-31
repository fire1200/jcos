"""첫말⑨ 모자 쓰고 신발 신고 (옷 입기)"""
import math
from kids.engine import *
from kids.fw_scene import make_song
from kids.fw_chars2 import shirt, shoes, hat
def _f(fn, s):
    return lambda f, x, y, sc, kind, t: paste(f, fn(s, kind), x, y, scale=sc, rot=4 * math.sin(t * 4))
def _sock(f, x, y, sc, kind, t): paste(f, sock(110, kind), x, y, scale=sc, rot=8 * math.sin(t * 4))
WORDS = {"옷": _f(shirt, 110), "양말": _sock, "신발": _f(shoes, 100), "모자": _f(hat, 110)}
setup, draw = make_song("모자 쓰고 신발 신고", WORDS, {}, ((225, 238, 255), (250, 250, 255)), (120, 120, 210), hide="closet")
