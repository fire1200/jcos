"""첫말④ 멍멍 야옹 누가 왔나"""
from kids.engine import *
from kids.fw_scene import make_song
from kids.fw_chars import cow, pig, chick
def _a(fn, s=120): return lambda f, x, y, sc, kind, t: paste(f, fn(s, kind), x, y, scale=sc)
pup, kit, ox, pg, ck = _a(lambda s, k: puppy(s, k)), _a(lambda s, k: cat(s, k)), _a(cow), _a(pig), _a(chick, 110)
WORDS = {"멍멍이": pup, "멍멍": pup, "야옹이": kit, "야옹": kit, "소": ox, "음매": ox, "돼지": pg, "꿀꿀": pg, "병아리": ck, "삐약": ck}
LAB = {"멍멍": "멍멍!", "야옹": "야옹!", "음매": "음매~", "꿀꿀": "꿀꿀!", "삐약": "삐약!"}
setup, draw = make_song("멍멍 야옹 누가 왔나", WORDS, LAB, ((205, 235, 200), (245, 252, 240)), (110, 160, 90), hide="fence")
