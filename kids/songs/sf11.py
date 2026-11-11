"""첫말⑪ 데굴데굴 공 어디 갔나 (장난감)"""
import math
from kids.engine import *
from kids.fw_scene import make_song
from kids.fw_chars2 import ball, blocks, rattle
def _ball(f, x, y, sc, kind, t): paste(f, ball(110, kind), x + 40 * math.sin(t * 2), y, scale=sc, rot=-t * 120)      # 데굴데굴
def _bear(f, x, y, sc, kind, t): paste(f, bear(110, kind), x, y, scale=sc, rot=4 * math.sin(t * 3))
def _blocks(f, x, y, sc, kind, t): paste(f, blocks(105, kind), x, y, scale=sc)
def _rattle(f, x, y, sc, kind, t): paste(f, rattle(95, kind), x, y, scale=sc, rot=18 * math.sin(t * 9))             # 딸랑딸랑
WORDS = {"공": _ball, "곰돌이": _bear, "블록": _blocks, "딸랑이": _rattle}
setup, draw = make_song("데굴데굴 공 어디 갔나", WORDS, {}, ((255, 236, 210), (255, 250, 240)), (230, 130, 80), hide="toybox")
