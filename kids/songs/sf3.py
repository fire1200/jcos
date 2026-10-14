"""첫말③ 맘마 냠냠"""
import math
from kids.engine import *
from kids.fw_scene import make_song
from kids.fw_chars import rice_bowl, water_cup, milk_bottle, spoon, baby_cloud
def _item(fn, s):
    def d(f, x, y, sc, kind, t):
        paste(f, fn(s), x, y, scale=sc)
    return d
def _please(f, x, y, sc, kind, t):          # 주세요: 몽이가 두 손 모으듯 숟가락을 들고 고개 끄덕
    paste(f, baby_cloud(95, "laugh"), x, y + 6 * math.sin(t * 6), scale=sc)
    paste(f, spoon(70), x + 170 * sc, y - 20, scale=sc, rot=20 * math.sin(t * 4))
WORDS = {"맘마": _item(rice_bowl, 120), "물": _item(water_cup, 120), "우유": _item(milk_bottle, 110), "주세요": _please, "냠냠": _item(rice_bowl, 120)}
setup, draw = make_song("맘마 냠냠", WORDS, {"냠냠": "냠냠!"}, ((255, 238, 200), (255, 250, 235)), (225, 140, 60), hide="blanket")
