"""유튜브 자동 동기화로 받은 .srt/.sbv → 가사 줄 시각 json.

자막 한 칸에 가사 줄이 여러 개 묶여 있으면 글자 수 비율로 나누고,
각 줄의 구간 이름(Verse/Chorus…)은 Suno 가사 태그에서 순서대로 가장 비슷한 줄을 찾아 붙인다.
사용: python -m kids.srt kids01.srt k01.meta out.json
"""
import re, sys, json
from kids.align import parse_meta, norm, _score

def parse_time(s):
    s = s.strip().replace(",", ".")
    parts = s.split(":")
    if len(parts) == 2: parts = ["0"] + parts
    h, m, sec = parts
    return int(h) * 3600 + int(m) * 60 + float(sec)

def read_cues(path):
    text = open(path, encoding="utf-8-sig").read().replace("\r", "")
    cues = []
    for block in re.split(r"\n\s*\n", text.strip()):
        rows = [r for r in block.split("\n") if r.strip()]
        if rows and rows[0].strip().isdigit(): rows = rows[1:]
        if not rows: continue
        m = re.match(r"([\d:.,]+)\s*(?:-->|,)\s*([\d:.,]+)", rows[0])
        if not m: continue
        cues.append((parse_time(m.group(1)), parse_time(m.group(2)), [r.strip() for r in rows[1:] if r.strip()]))
    return cues

def to_lines(cues, meta_lines):
    out, pos = [], 0
    for t0, t1, rows in cues:
        total = sum(len(norm(r)) or 1 for r in rows); acc = 0
        for r in rows:
            key = "".join(norm(r)); start = t0 + (t1 - t0) * acc / total; acc += len(norm(r)) or 1
            best, bi = -9, None
            for k in range(pos, min(len(meta_lines), pos + 10)):
                sc = _score(key, "".join(norm(meta_lines[k]["text"]))) if key else -9
                if sc > best: best, bi = sc, k
            sec = meta_lines[bi]["section"] if bi is not None and best > 0.3 else (out[-1]["section"] if out else "Verse 1")
            if bi is not None and best > 0.3: pos = bi + 1
            out.append(dict(section=sec, text=r, start=round(start, 2), conf=1.0))
    return out

if __name__ == "__main__":
    cues = read_cues(sys.argv[1]); meta = parse_meta(sys.argv[2])
    res = to_lines(cues, meta)
    json.dump(res, open(sys.argv[3], "w"), ensure_ascii=False, indent=1)
    for r in res: print(f"{r['start']:7.2f} [{r['section']}] {r['text']}")


def to_lines_refined(cues, meta_lines, obs):
    """자막 한 칸에 여러 줄이 묶여 있으면, 그 칸 시간 범위 안에서 음성 인식 관측값으로 각 줄의 시작을 찾는다.
    못 찾으면 글자 수 비율. 첫 줄은 칸 시작 시각 (유튜브 동기화가 가장 정확한 부분)."""
    good = [o for o in obs if o["t0"] - o["win"] > 0.25 and "[" not in o["text"] and "(" not in o["text"]]
    base = to_lines(cues, meta_lines)  # 구간 이름과 비율 추정
    out, k = [], 0
    for t0, t1, rows in cues:
        prev = t0 - 1
        for j, r in enumerate(rows):
            b = base[k]; k += 1
            if j == 0:
                start = t0
            else:
                key = "".join(norm(r)); cands = []
                for o in good:
                    if not (t0 + 0.3 <= o["t0"] <= t1 - 0.4): continue
                    x = "".join(norm(o["text"]))[: int(len(key) * 1.3) + 1]
                    if len(x) >= max(1, len(key) * 0.5) and _score(x, key) >= 0.4: cands.append(o["t0"])
                cands = sorted(c for c in cands if c > prev + 0.6)
                start = cands[0] if cands else max(b["start"], prev + 0.8)
            start = min(start, t1 - 0.3)
            out.append(dict(section=b["section"], text=r, start=round(start - 0.05, 2), conf=1.0))
            prev = start
    return out


def fix_sections(lines):
    """가사 태그에 [Outro]가 곡 중간(전주 등)에 잘못 붙은 경우, 앞 줄의 구간 이름으로 바꾼다."""
    for i, l in enumerate(lines):
        if l["section"] == "Outro" and any(x["section"] != "Outro" for x in lines[i + 1:]):
            l["section"] = lines[i - 1]["section"] if i > 0 else "Intro"
    return lines
