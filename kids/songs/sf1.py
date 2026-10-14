"""첫말① 엄마 아빠 어디 있나"""
from kids.engine import *
from kids.fw_scene import make_song
from kids.fw_chars import mom, dad, grandma, grandpa
def _p(fn): return lambda f, x, y, sc, kind, t: paste(f, fn(110, kind), x, y, scale=sc)
WORDS = {"엄마": _p(mom), "아빠": _p(dad), "할머니": _p(grandma), "할아버지": _p(lambda s, k: grandpa(s, k))}
setup, draw = make_song("엄마 아빠 어디 있나", WORDS, {}, ((255, 222, 205), (255, 245, 238)), (235, 120, 130))
