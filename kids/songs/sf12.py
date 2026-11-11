"""첫말⑫ 아야 호~ 괜찮아 (마음 말) — 아기 몽이가 콩 넘어지고, 엄마 구름이 호~ 해 주고 안아 줍니다."""
import math
from kids.engine import *
from kids.fw_scene import make_song
from kids.fw_chars import baby, mom
def _aya(f, x, y, sc, kind, t):                        # 넘어져서 무릎을 짚는 아기 + 작은 별
    paste(f, baby(95, "stand", None, "o"), x, y - 60, scale=sc * 0.85, rot=-8)
    for k in range(3): paste(f, star(16, (255, 220, 90)), x + 120 * sc + 30 * math.cos(t * 4 + k * 2), y - 260 * sc + 20 * math.sin(t * 4 + k * 2))
def _ho(f, x, y, sc, kind, t):                         # 엄마 구름이 호~ 불어 줌
    paste(f, baby(95, "stand", None, "smile"), x + 120 * sc, y - 60, scale=sc * 0.8)
    paste(f, mom(85, "o"), x - 200 * sc, y - 120, scale=sc)
    for k in range(3):
        q = (t * 0.8 + k / 3) % 1
        paste(f, plain_cloud(14 + 6 * k, (230, 240, 255), shadow=False), x - 60 * sc + 160 * q * sc, y - 150 - 20 * k, alpha=1 - q)
def _ttuk(f, x, y, sc, kind, t):                       # 눈물 뚝 — 눈물 닦고 웃음
    paste(f, baby(95, "eye", None, "smile"), x, y - 60, scale=sc * 0.85)
def _ok(f, x, y, sc, kind, t):                         # 괜찮아 — 엄마랑 꼭
    paste(f, mom(100, "laugh"), x - 110 * sc, y - 60, scale=sc)
    paste(f, baby(80, "hands_up", None, "laugh"), x + 110 * sc, y - 30, scale=sc * 0.85)
    paste(f, big_text("♥", 70, (255, 130, 160), (255, 255, 255)), x, y - 300 * sc + 10 * math.sin(t * 3))
WORDS = {"아야": _aya, "호": _ho, "뚝": _ttuk, "괜찮아": _ok}
LAB = {"아야": "아야!", "호": "호~", "뚝": "뚝!", "괜찮아": "괜찮아"}
setup, draw = make_song("아야 호~ 괜찮아", WORDS, LAB, ((255, 225, 230), (255, 248, 245)), (225, 110, 140), hide="cloud", zoom=1.3)
