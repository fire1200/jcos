"""모음 영상: 몽글이 인사 → (몽글이의 다음 곡 소개 → 곡) × N → 마무리 인사.
사용: python -m kids.compile OUT.mp4 "제목" 01 03 05 ...   (환경변수 FINAL=본편 폴더, THUMBS=썸네일 폴더, NIGHT=1 잠자리 모음)
"""
import sys, os, glob, subprocess, json, math
from kids import engine
from kids.engine import *
from kids.thumbs import TITLES

FINAL = os.environ["FINAL"]; THUMBS = os.environ["THUMBS"]; TMP = os.environ.get("TMPDIR_K", "/tmp/kc")
NIGHT = os.environ.get("NIGHT") == "1"
SKY = vgrad((24, 30, 78), (78, 74, 140)) if NIGHT else vgrad((140, 205, 250), (222, 241, 255))
INK = (70, 70, 140) if NIGHT else (95, 140, 225)   # 글자 테두리
CHIME = "aevalsrc='" + ("0.10" if NIGHT else "0.25") + "*(sin(2*PI*1047*t)*exp(-4*t)+if(gte(t,0.22),sin(2*PI*1319*(t-0.22))*exp(-4*(t-0.22)),0)+if(gte(t,0.44),sin(2*PI*1568*(t-0.44))*exp(-3*(t-0.44)),0))':s=48000:d={d}"

def dur(p):
    out = subprocess.run([engine.FFMPEG, "-i", p], capture_output=True, text=True).stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", out).groups(); return int(h) * 3600 + int(m) * 60 + float(s)

def card(path, seconds, drawer):
    p = subprocess.Popen([engine.FFMPEG, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                          "-f", "lavfi", "-i", CHIME.format(d=seconds), "-filter_complex", "[1:a]aformat=channel_layouts=stereo,afade=t=out:st=%.2f:d=0.5[a]" % (seconds - 0.5),
                          "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-t", f"{seconds}", path], stdin=subprocess.PIPE)
    for i in range(int(seconds * 30)):
        p.stdin.write(drawer(i / 30).convert("RGB").tobytes())
    p.stdin.close(); p.wait()

STARS = [((i * 397) % W, (i * 211) % 620 + 30, 6 + i % 4, i * 0.7) for i in range(40)]

def clouds(f, t):
    if NIGHT:
        for x, y, r, ph in STARS:
            paste(f, star(r, (255, 236, 170)), x, y, alpha=0.45 + 0.4 * (0.5 + 0.5 * math.sin(t * 2 + ph)))
        paste(f, moon(70), 1700, 170)
        for i, (y, s, sp, ph) in enumerate([(330, 50, 10, 0), (880, 60, 12, 900)]):
            paste(f, plain_cloud(s), (ph + t * sp) % (W + 500) - 250, y, alpha=0.35)
        return
    for i, (y, s, sp, ph) in enumerate([(150, 70, 22, 0), (300, 50, 30, 700), (880, 60, 26, 1300)]):
        paste(f, plain_cloud(s), (ph + t * sp) % (W + 500) - 250, y)

def intro_drawer(title):
    def d(t):
        f = SKY.copy(); clouds(f, t)
        paste(f, cloud_char(170, "smile" if NIGHT else "laugh"), 560, 520 + bob(t, 18, 1.4), rot=(2 if NIGHT else 6) * math.sin(t * 3))
        paste(f, big_text("안녕! 나는 몽글이야", 90, (255, 255, 255), INK), 1250, 400, alpha=min(1, t / 0.4))
        paste(f, big_text(title, 110, (255, 240, 120), INK), 1250, 560, alpha=min(1, max(0, t - 0.8) / 0.4))
        paste(f, big_text("포근히 누워서 들어 볼까?" if NIGHT else "같이 불러 볼까?", 80, (255, 255, 255), INK if NIGHT else (232, 120, 160)), 1250, 720, alpha=min(1, max(0, t - 1.8) / 0.4))
        return f
    return d

def next_drawer(n, idx):
    th = Image.open(glob.glob(f"{THUMBS}/kids{n}_thumb.jpg")[0]).convert("RGBA").resize((880, 495))
    m = Image.new("L", th.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, th.width, th.height], 40, fill=255); th.putalpha(m)
    fr = new_layer(th.width + 24, th.height + 24); ImageDraw.Draw(fr).rounded_rectangle([0, 0, fr.width, fr.height], 50, fill=(255, 255, 255, 255)); fr.alpha_composite(th, (12, 12))
    fr = soft_shadow(fr, dx=0, dy=14, alpha=70, blur=14)
    a, b = TITLES[n]
    def d(t):
        f = SKY.copy(); clouds(f, t)
        paste(f, cloud_char(120, "o" if t < 1.2 else "laugh"), 330, 560 + bob(t, 16, 1.2))
        paste(f, big_text(f"{idx}번째 노래는?", 80, (255, 255, 255), INK), 330, 300, alpha=min(1, t / 0.3))
        k = ease(max(0, t - 0.5) / 0.5)
        paste(f, fr, 1220, 520, scale=0.6 + 0.4 * k, alpha=k)
        paste(f, big_text(f"{a} {b}", 84, (255, 240, 120), INK), 1220, 900, alpha=min(1, max(0, t - 1.0) / 0.4))
        return f
    return d

def outro_drawer():
    def d(t):
        f = SKY.copy(); clouds(f, t)
        for j, (x, k) in enumerate([(560, "laugh"), (960, "smile"), (1360, "laugh")]):
            paste(f, cloud_char(110 if j == 1 else 90, k, (255, 255, 255) if j != 1 else (255, 215, 230)), x, 470 + bob(t, 14, 1.3, j))
        paste(f, big_text("오늘도 고마워, 잘 자요" if NIGHT else "같이 불러 줘서 고마워!", 100, (255, 255, 255), INK), 960, 760, alpha=min(1, t / 0.4))
        paste(f, big_text("좋은 꿈 꿔요~ 몽글구름 동요" if NIGHT else "또 만나요~ 몽글구름 동요", 76, (255, 240, 120), INK if NIGHT else (232, 120, 160)), 960, 900, alpha=min(1, max(0, t - 0.8) / 0.4))
        return f
    return d

if __name__ == "__main__":
    out, title, songs = sys.argv[1], sys.argv[2], sys.argv[3:]
    os.makedirs(TMP, exist_ok=True)
    parts = []
    card(f"{TMP}/intro.mp4", 5.0, intro_drawer(title)); parts.append(("intro", f"{TMP}/intro.mp4"))
    for i, n in enumerate(songs, 1):
        card(f"{TMP}/next{i:02d}_{n}.mp4", 4.0, next_drawer(n, i)); parts.append(("next", f"{TMP}/next{i:02d}_{n}.mp4"))
        parts.append((n, glob.glob(f"{FINAL}/kids{n}_*.mp4")[0]))
    card(f"{TMP}/outro.mp4", 6.0, outro_drawer()); parts.append(("outro", f"{TMP}/outro.mp4"))
    # 챕터 시각
    t, chapters = 0.0, []
    for kind, p in parts:
        if kind == "intro": chapters.append((t, "시작 인사"))
        elif kind == "next": pass
        elif kind == "outro": chapters.append((t, "마무리 인사"))
        else: chapters.append((t - 4.0, " ".join(TITLES[kind])))
        t += dur(p)
    ins = []
    for _, p in parts: ins += ["-i", p]
    fc = "".join(f"[{i}:v]fps=30,format=yuv420p,setsar=1[v{i}];[{i}:a]aresample=48000,aformat=channel_layouts=stereo[a{i}];" for i in range(len(parts)))
    fc += "".join(f"[v{i}][a{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=1:a=1[v][a]"
    subprocess.run([engine.FFMPEG, "-v", "error", "-y", *ins, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                    "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out], check=True)
    json.dump([(round(a, 1), b) for a, b in chapters], open(out + ".chapters.json", "w"), ensure_ascii=False)
    for a, b in chapters: print(f"{int(a // 60)}:{int(a % 60):02d} {b}")
    print("total", round(t, 1))
