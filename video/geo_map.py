"""지리송 화면 왼쪽에 들어갈 지도 판을 그립니다 (실제 행정경계 자료, 통계청 2013 시도 경계).

    from geo_map import MapPanel
    p = MapPanel(font_path)
    img = p.draw(highlight=["경기도"], pins=["수원"], title="경기도청: 수원")   # RGBA
"""
import json
import math
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "geo_data", "skorea_provinces_2013.json")
OLD_DATA = os.path.join(HERE, "geo_data", "korea_peninsula_ne10m.json")   # 한반도 전체 (Natural Earth 10m)
# 옛 지방(조선 8도 기준) → 지금 시도 (대략, 옛 경계와 꼭 같지는 않음)
OLD = {"관북": ["함경북도", "함경남도", "라선특별시", "량강도"], "관서": ["평안북도", "평안남도", "평양직할시", "자강도"],
       "해서": ["황해북도", "황해남도"], "관동": ["강원도", "강원도(북)"], "경기": ["서울특별시", "인천광역시", "경기도"],
       "호서": ["충청남도", "충청북도", "대전광역시", "세종특별자치시"], "호남": ["전라북도", "전라남도", "광주광역시"],
       "영남": ["경상북도", "경상남도", "대구광역시", "울산광역시", "부산광역시"]}
OLD["기호"] = OLD["경기"] + OLD["호서"]
OLD_COL = {"관북": (120, 170, 220), "관서": (150, 200, 120), "해서": (230, 190, 90), "관동": (120, 200, 200),
           "경기": (240, 140, 120), "호서": (190, 150, 220), "호남": (240, 170, 80), "영남": (220, 120, 160)}
# 영동·영서를 가르는 태백산맥 줄기 (강원 구간, 대략)
RIDGE = [(128.25, 38.62), (128.42, 38.25), (128.58, 37.92), (128.72, 37.68), (128.9, 37.5), (129.02, 37.3), (128.98, 37.08)]

# 노래에서 부르는 짧은 이름 → 자료 속 이름
ALIAS = {"서울": "서울특별시", "인천": "인천광역시", "경기": "경기도", "강원": "강원도", "충북": "충청북도", "충남": "충청남도",
         "대전": "대전광역시", "세종": "세종특별자치시", "전북": "전라북도", "전남": "전라남도", "광주": "광주광역시",
         "제주": "제주특별자치도", "경북": "경상북도", "경남": "경상남도", "대구": "대구광역시", "울산": "울산광역시",
         "부산": "부산광역시"}
# 도청 소재지·시 (경도, 위도)
PLACES = {"수원": (127.05, 37.29), "춘천": (127.73, 37.88), "청주": (127.49, 36.64), "홍성": (126.67, 36.66),
          "전주": (127.11, 35.82), "무안": (126.46, 34.81), "안동": (128.50, 36.57), "창원": (128.69, 35.24),
          "제주시": (126.50, 33.49), "서울": (126.98, 37.57), "인천": (126.70, 37.46), "대전": (127.38, 36.35),
          "세종": (127.29, 36.48), "광주": (126.85, 35.16), "대구": (128.60, 35.87), "울산": (129.31, 35.54),
          "부산": (129.08, 35.18), "한양": (126.98, 37.57), "철령관": (127.43, 38.92), "대관령": (128.72, 37.68),
          "조령": (128.07, 36.79)}
KIND = {"서울특별시": "특별시", "세종특별자치시": "특별자치시", "인천광역시": "광역시", "대전광역시": "광역시",
        "광주광역시": "광역시", "대구광역시": "광역시", "울산광역시": "광역시", "부산광역시": "광역시",
        "강원도": "특별자치도", "전라북도": "특별자치도", "제주특별자치도": "특별자치도"}
KIND_COL = {"특별시": (255, 120, 120), "특별자치시": (255, 170, 90), "광역시": (120, 180, 255), "도": (140, 210, 140),
            "특별자치도": (200, 150, 240)}
BASE, LINE, HI = (250, 240, 214), (150, 120, 90), (255, 150, 40)
SEA = (205, 232, 245)


class MapPanel:
    def __init__(self, font_path, w=600, h=760, old=False):
        """old=True: 2곡용 한반도 전체 옛 지도 (한지 색)."""
        self.w, self.h, self.old = w, h, old
        self.font_path = font_path
        feats = json.load(open(OLD_DATA if old else DATA, encoding="utf-8"))["features"]
        self.shapes = {}
        for f in feats:
            g = f["geometry"]
            polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
            name = f["properties"]["name"]
            if f["properties"].get("country") == "PRK" and name == "강원도":
                name = "강원도(북)"
            self.shapes.setdefault(name, []).extend(p[0] for p in polys)
        lons = [x for ps in self.shapes.values() for p in ps for x, y in p]
        lats = [y for ps in self.shapes.values() for p in ps for x, y in p]
        self.k = math.cos(math.radians(38 if old else 36))
        self.full = (min(lons), min(lats), max(lons), max(lats))
        self.view(self.full)

    def view(self, box):
        """box=(서경, 남위, 동경, 북위) 영역이 판에 꽉 차게."""
        x0, y0, x1, y1 = box[0] * self.k, box[1], box[2] * self.k, box[3]
        pad, top = 30, 110
        self.s = min((self.w - 2 * pad) / (x1 - x0), (self.h - top - pad) / (y1 - y0))
        self.ox = (self.w - (x1 - x0) * self.s) / 2 - x0 * self.s
        self.oy = top + (self.h - top - pad - (y1 - y0) * self.s) / 2 + y1 * self.s
        self.cache = {}

    def xy(self, lon, lat):
        return self.ox + lon * self.k * self.s, self.oy - lat * self.s

    def font(self, size):
        return ImageFont.truetype(self.font_path, size)

    def draw(self, highlight=(), pins=(), title="", kinds=False, glow=1.0, ridge=False, labels=(), box=None):
        """highlight: 칠할 시도(1곡) 또는 옛 지방 이름(2곡), pins: 핀 꽂을 곳,
        kinds: 종류별 색칠(1곡 총정리) / 옛 지방 8곳 색칠(2곡 총정리), glow: 0~1 반짝임 세기, ridge: 태백산맥 줄기."""
        self.view(box or self.full)
        hl = set()
        for n in highlight:
            hl |= set(OLD[n]) if self.old and n in OLD else {ALIAS.get(n, n)}
        im = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, self.w - 1, self.h - 1), 36, fill=255)
        d = ImageDraw.Draw(im)
        sea = (196, 214, 210) if self.old else SEA
        d.rounded_rectangle((0, 0, self.w - 1, self.h - 1), 36, fill=sea + (240,), outline=(255, 255, 255, 255), width=6)
        polys = {n: [[self.xy(x, y) for x, y in p] for p in ps] for n, ps in self.shapes.items()}
        # 반짝임: 칠한 곳 둘레에 흐린 빛
        if hl and glow > 0:
            gl = Image.new("RGBA", im.size, (0, 0, 0, 0))
            gd = ImageDraw.Draw(gl)
            for n in hl:
                for p in polys[n]:
                    gd.polygon(p, fill=(255, 230, 120, int(255 * glow)))
            im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(14)))
            d = ImageDraw.Draw(im)
        old_of = {m: k for k, v in OLD.items() if k != "기호" for m in v}
        for n, ps in polys.items():
            if n in hl:
                col = (215, 90, 50) if self.old else HI
            elif kinds:
                col = OLD_COL.get(old_of.get(n), (244, 232, 200)) if self.old else KIND_COL[KIND.get(n, "도")]
            else:
                col = (244, 232, 200) if self.old else BASE
            for p in ps:
                d.polygon(p, fill=col, outline=None if self.old else LINE)
        if self.old:   # 옛 지도는 지금 시도 경계 대신 옛 지방 경계만 굵게
            for k, members in OLD.items():
                if k == "기호":
                    continue
                for m in members:
                    for p in polys.get(m, []):
                        d.line(p + [p[0]], fill=(150, 120, 90), width=1)
        if ridge:
            pts = [self.xy(*c) for c in RIDGE]
            d.line(pts, fill=(60, 40, 30), width=6, joint="curve")
            for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                mx, my = (x0 + x1) / 2, (y0 + y1) / 2
                d.polygon([(mx - 13, my + 9), (mx, my - 14), (mx + 13, my + 9)], fill=(60, 40, 30))
        for n in hl:   # 칠한 곳 테두리를 굵게
            for p in polys[n]:
                d.line(p + [p[0]], fill=(200, 80, 0), width=4, joint="curve")
        boxes = []
        for name in pins:
            x, y = self.xy(*PLACES[name])
            d.ellipse((x - 13, y - 13, x + 13, y + 13), fill=(230, 50, 60), outline=(255, 255, 255), width=4)
        for name in pins:   # 이름표가 겹치면 핀 아래로
            x, y = self.xy(*PLACES[name])
            f = self.font(34)
            tw = d.textlength(name, font=f)
            bx = min(max(x - tw / 2, 10), self.w - tw - 10)
            box = (bx - 10, y - 66, bx + tw + 10, y - 20)
            if any(b[0] < box[2] and box[0] < b[2] and b[1] < box[3] and box[1] < b[3] for b in boxes):
                box = (bx - 10, y + 20, bx + tw + 10, y + 66)
            boxes.append(box)
            d.rounded_rectangle(box, 14, fill=(255, 255, 255, 240))
            d.text((bx, (box[1] + box[3]) / 2), name, font=f, fill=(60, 40, 30), anchor="lm")
        for text, lon, lat in labels:
            x, y = self.xy(lon, lat)
            d.text((x, y), text, font=self.font(40), fill=(60, 40, 30), anchor="mm", stroke_width=5, stroke_fill=(255, 255, 255))
        if title:
            f = self.font(48)
            d.text((self.w / 2, 58), title, font=f, fill=(60, 40, 30), anchor="mm", stroke_width=6, stroke_fill=(255, 255, 255))
        if kinds and self.old:
            f = self.font(26)
            for k, members in OLD.items():
                if k == "기호":
                    continue
                pts = [pt for m in members for p in polys.get(m, []) for pt in p]
                cx = sum(x for x, y in pts) / len(pts)
                cy = sum(y for x, y in pts) / len(pts)
                d.text((cx, cy), k, font=f, fill=(60, 40, 30), anchor="mm", stroke_width=4, stroke_fill=(255, 255, 255))
        elif kinds:
            y = self.h - 34
            x = 24
            f = self.font(24)
            for k, c in KIND_COL.items():
                d.rounded_rectangle((x, y - 12, x + 22, y + 10), 5, fill=c, outline=LINE)
                d.text((x + 28, y), k, font=f, fill=(60, 40, 30), anchor="lm")
                x += 34 + d.textlength(k, font=f) + 14
        im.putalpha(Image.composite(im.getchannel("A"), Image.new("L", im.size, 0), mask))
        ImageDraw.Draw(im).rounded_rectangle((0, 0, self.w - 1, self.h - 1), 36, outline=(255, 255, 255, 255), width=6)
        return im
