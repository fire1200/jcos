"""곡별 썸네일 (1280x720): 후렴 장면 한 컷 + 큰 제목. 사용: python -m kids.thumbs NN audio lines.json out.jpg"""
import sys, json, importlib
from kids import engine
from kids.engine import *
from kids.make import duration

TITLES = {"01": ("구름 빵빵", "방귀 풍선"), "02": ("솜사탕", "비가 내려요"), "03": ("아기 공룡", "쿵쾅쿵쾅"), "04": ("반짝별 요정의", "자장가"),
          "05": ("무지개", "미끄럼틀 슝슝"), "06": ("장난감 친구들의", "밤마실"), "07": ("개구쟁이", "양말 한 짝"), "08": ("비눗방울 타고", "바다 여행"),
          "09": ("도토리 톡!", "다람쥐 콩!"), "10": ("꼭꼭 숨어라", "그림자야"),
          "11": ("빵빵 붕붕", "출발 자동차"), "12": ("치카치카", "거품 괴물"), "13": ("바스락", "낙엽 비"), "14": ("흔들흔들", "멈춰!")}
STROKE = {"01": (95, 140, 225), "02": (232, 120, 160), "03": (90, 160, 90), "04": (90, 90, 170), "05": (110, 140, 230), "06": (120, 110, 190),
          "07": (230, 110, 120), "08": (80, 150, 220), "09": (200, 120, 60), "10": (110, 150, 220),
          "11": (240, 95, 95), "12": (90, 170, 210), "13": (210, 120, 60), "14": (230, 120, 170)}

if __name__ == "__main__":
    n, audio, lines, out = sys.argv[1:5]
    mod = importlib.import_module(f"kids.songs.s{n}")
    total = duration(audio); L = json.load(open(lines)); ctx = mod.setup(L, total)
    ch = [s for s in ctx["sp"] if s[0] == "Chorus"] or ctx["sp"]
    t = ch[0][1] + min(6, (ch[0][2] - ch[0][1]) * 0.5)
    ctx = dict(ctx, sched=[])
    f = mod.draw(t, ctx)
    a, b = TITLES[n]
    top = n in ("03", "06", "07", "09", "10", "11", "13", "14")  # 캐릭터가 아래쪽에 있는 곡은 제목을 위로
    y1, y2 = (150, 330) if top else (H - 330, H - 150)
    paste(f, big_text(a, 170, (255, 255, 255), STROKE[n]), W / 2, y1)
    paste(f, big_text(b, 190, (255, 240, 120), STROKE[n]), W / 2, y2)
    f.convert("RGB").resize((1280, 720), Image.LANCZOS).save(out, quality=92)
