"""첫말⑦ 부릉부릉 누가 오나 (탈것)"""
import math
from kids.engine import *
from kids.fw_scene import make_song
from kids.s2_chars import toy_car, bus as _bus
from kids.fw_chars2 import airplane
def _car(f, x, y, sc, kind, t): paste(f, toy_car(120, ang=t * 400, kind=kind), x, y, scale=sc)
def _bus_(f, x, y, sc, kind, t): paste(f, _bus(105, kind, ang=t * 300), x, y, scale=sc)
def _train(f, x, y, sc, kind, t): paste(f, train(95, wheel=t * 6), x, y, scale=sc)
def _plane(f, x, y, sc, kind, t): paste(f, airplane(105, kind), x, y - 30, scale=sc, rot=4 * math.sin(t * 3))
WORDS = {"자동차": _car, "버스": _bus_, "기차": _train, "비행기": _plane}
LAB = {"자동차": "자동차", "버스": "버스", "기차": "기차", "비행기": "비행기"}
setup, draw = make_song("부릉부릉 누가 오나", WORDS, LAB, ((190, 225, 250), (240, 250, 240)), (80, 140, 210), hide="tunnel", zoom=1.4)
