"""첫말⑧ 사과 바나나 냠냠 (과일)"""
import math
from kids.engine import *
from kids.fw_scene import make_song
from kids.fw_chars2 import apple, banana, strawberry, grapes
def _f(fn, s):
    return lambda f, x, y, sc, kind, t: paste(f, fn(s, kind), x, y + 8 * math.sin(t * 5), scale=sc)
WORDS = {"사과": _f(apple, 110), "바나나": _f(banana, 105), "딸기": _f(strawberry, 110), "포도": _f(grapes, 105)}
setup, draw = make_song("사과 바나나 냠냠", WORDS, {}, ((255, 228, 220), (255, 248, 240)), (225, 95, 110), hide="basket")
