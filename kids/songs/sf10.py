"""첫말⑩ 해님 꽃님 안녕 (바깥·자연)"""
import math
from kids.engine import *
from kids.fw_scene import make_song
def _sun(f, x, y, sc, kind, t): paste(f, sun(110, kind), x, y - 40, scale=sc, rot=6 * math.sin(t * 2))
def _flower(f, x, y, sc, kind, t): paste(f, flower(120, kind=kind), x, y, scale=sc, rot=6 * math.sin(t * 3))
def _tree(f, x, y, sc, kind, t): paste(f, tree(130), x, y - 20, scale=sc, rot=3 * math.sin(t * 2))
def _bird(f, x, y, sc, kind, t): paste(f, bird(110, kind), x, y - 30 + 20 * math.sin(t * 4), scale=sc)
WORDS = {"해": _sun, "꽃": _flower, "나무": _tree, "새": _bird}
setup, draw = make_song("해님 꽃님 안녕", WORDS, {}, ((180, 220, 250), (235, 248, 225)), (90, 160, 90), hide="cloud", ignore=("냄새",))
