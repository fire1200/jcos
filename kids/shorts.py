"""세로 쇼츠 (1080x1920, 후렴 약 40초). 사용: python -m kids.shorts NN audio lines.json out.mp4 [--preview t,...]

가로 장면을 세로 가운데에 크게 잘라 넣고, 위에는 제목, 아래에는 가사 자막.
"""
import sys, json, importlib, subprocess
from kids import engine
from kids.engine import *
from kids.make import duration
from kids.thumbs import TITLES, STROKE

SW, SH = 1080, 1920
LEN = 40.0

def pick_window(ctx, total):
    ch = [s for s in ctx["sp"] if s[0] == "Chorus"]
    t0 = max(0.0, (ch[0][1] if ch else ctx["sp"][0][1]) - 1.5)
    return t0, min(LEN, total - t0)

@lru_cache(maxsize=None)
def bg_band(col):
    return Image.new("RGBA", (SW, SH), col + (255,))

def frame(mod, ctx_scene, sched, t, n, t0, dur):
    scene = mod.draw(t, ctx_scene)              # 자막 없는 가로 장면
    sc = scene.resize((2133, 1200), Image.BILINEAR).crop((526, 0, 526 + SW, 1200))
    f = bg_band(tuple(max(0, v - 25) for v in scene.getpixel((960, 20))[:3])).copy()
    f.alpha_composite(sc, (0, 360))
    a, b = TITLES[n]
    f.alpha_composite(big_text(a, 92, (255, 255, 255), STROKE[n]), (int(SW / 2 - big_text(a, 92, (255, 255, 255), STROKE[n]).width / 2), 70))
    bt = big_text(b, 110, (255, 240, 120), STROKE[n]); f.alpha_composite(bt, (int(SW / 2 - bt.width / 2), 190))
    # 자막 (아래 띠)
    for i, (s, e, text, _) in enumerate(sched):
        if s <= t < e:
            al = min(1.0, (t - s) / 0.2, (e - t) / 0.2)
            cap = caption_img(text)
            if cap.width > SW - 40: cap = cap.resize((SW - 40, int(cap.height * (SW - 40) / cap.width)), Image.BILINEAR)
            paste(f, cap, SW / 2, 1660, alpha=max(0, al))
            if i + 1 < len(sched) and sched[i + 1][0] - e < 1.0 and sched[i + 1][2] != text:
                nx = next_img(sched[i + 1][2]); paste(f, nx, SW / 2, 1790, alpha=0.85 * max(0, al))
            break
    # 끝 1.5초: "전체 노래는 채널에서" 안내
    if t > t0 + dur - 2.5:
        paste(f, big_text("전체 노래는 채널에서!", 64, (255, 255, 255), STROKE[n]), SW / 2, 1520, alpha=min(1, (t - (t0 + dur - 2.5)) / 0.4))
    return f

if __name__ == "__main__":
    n, audio, lines, out = sys.argv[1:5]
    mod = importlib.import_module(f"kids.songs.s{n}")
    total = duration(audio); L = json.load(open(lines)); ctx = mod.setup(L, total)
    t0, dur = pick_window(ctx, total)
    sched = ctx["sched"]; ctx_scene = ctx; engine.CAPTIONS = False   # 장면은 가사에 맞춰 움직이되, 자막은 아래 띠에만
    if len(sys.argv) > 6 and sys.argv[5] == "--preview":
        for k in sys.argv[6].split(","):
            frame(mod, ctx_scene, sched, t0 + float(k), n, t0, dur).convert("RGB").save(f"{out}_{float(k):05.1f}.png")
        sys.exit()
    p = subprocess.Popen([engine.FFMPEG, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{SW}x{SH}", "-r", "30", "-i", "-",
                          "-ss", f"{t0:.2f}", "-t", f"{dur:.2f}", "-i", audio, "-map", "0:v", "-map", "1:a",
                          "-af", f"afade=t=in:d=0.4,afade=t=out:st={dur - 1.8:.2f}:d=1.8",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                          "-t", f"{dur:.2f}", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i in range(int(dur * 30)):
        p.stdin.write(frame(mod, ctx_scene, sched, t0 + i / 30, n, t0, dur).convert("RGB").tobytes())
    p.stdin.close(); p.wait()
    print(n, f"{t0:.1f}+{dur:.1f}")
