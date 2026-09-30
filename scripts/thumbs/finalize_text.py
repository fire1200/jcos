"""10/6~10/30 여덟 편의 설명·고정댓글 자리표시([ ])를 확정 문구로 채운다.

- publish CSV의 설명에서 안전 문구·재생목록 주소 자리표시를 바꿔 CSV를 갱신
- 업로드 때 복사해 붙일 전문(제목·설명·태그·고정댓글)을 txt 하나로 출력
사용: python scripts/thumbs/finalize_text.py OUT.txt
"""
import csv, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLAYLISTS_URL = "https://www.youtube.com/@dodamam/playlists"

SAFE_BABY = """· 소리는 옆 사람과 조용히 대화할 수 있을 만큼 작게 맞춰 주세요.
· 스마트폰·스피커는 아기 머리맡이 아니라 2m 이상 떨어진 곳에 두세요.
· 아기가 잠든 뒤에는 타이머로 끄거나 소리를 더 줄여 주세요.
· 이어폰·헤드폰으로 아기에게 직접 들려주지 마세요."""
SAFE_PRENATAL = """· 이어폰으로 들으실 때는 볼륨을 절반 이하로 맞춰 주세요.
· 스피커를 배에 직접 대지 마시고, 방 안에 편하게 틀어 두세요.
· 잠들기 전에 들으신다면 타이머를 맞춰 두시는 것을 권합니다."""
PIN_SAFE_BABY = """🔉 안전하게 들어 주세요
· 볼륨은 조용한 대화보다 작게
· 기기는 아기에게서 2m 이상 떨어진 곳에
· 잠든 뒤에는 타이머로 끄기"""
PIN_SAFE_PRENATAL = """🔉 편하게 들어 주세요
· 이어폰은 볼륨 절반 이하로
· 스피커를 배에 직접 대지 않기"""

DARK04_SONGS = "00:00 시작 — 노랫말 없는 피아노 자장가 14곡이 3시간 동안 끊김 없이 이어집니다"

VIDEOS = [  # (csv, 행 번호, 공개, 번호, 태그, 고정댓글 첫 줄, 고정댓글 끝 줄, 태교 여부)
    ("publish_dark04.csv", 0, "10/6 (화) 20:00", "#4 어두운 화면", "dark04_finish.md",
     "화면이 어두워 아기 옆에 켜 두셔도 눈부시지 않습니다 🌙",
     "새벽에 몇 번쯤 깨는지, 다시 잠드는 데 얼마나 걸리는지 댓글로 알려 주시면 다음 영상에 참고합니다.", False),
    ("publish_rain03.csv", 0, "10/9 (금) 20:00", "#3 비 오는 밤", "rain03_finish.md",
     "빗소리와 느린 심장박동이 밤새 끊김 없이 이어집니다 🌧",
     "빗소리가 더 큰 버전, 심장박동만 있는 버전 중 어떤 게 필요하신지 댓글로 알려 주세요.", False),
    ("publish_shush05.csv", 0, "10/13 (화) 20:00", "#5 쉬 소리", "shush05_finish.md",
     "쉬 소리와 빗소리, 개울물 소리가 밤새 끊김 없이 이어집니다 🌙",
     "쉬 소리만 있는 버전과 이 버전 중 어떤 게 아기에게 더 잘 맞는지 댓글로 알려 주세요.", False),
    ("publish_october_1016_1030.csv", 0, "10/16 (금) 20:00", "#6 태교음악", "october_1016_1030.md",
     "잠들기 전이나 쉬는 시간에 편하게 틀어 두세요 🌷",
     "아기가 태어난 뒤에는 '엄마 허밍 자장가' 재생목록도 함께 들어 보세요.", True),
    ("publish_october_1016_1030.csv", 1, "10/20 (화) 20:00", "#7 새벽 수유 후", "october_1016_1030.md",
     "새벽 수유 끝나고 불을 켜지 않은 채 틀어 두세요 🌙 2시간 동안 소리가 끊기지 않습니다.",
     "아기가 보통 몇 시쯤 깨는지 댓글로 알려 주시면 다음 영상 길이를 정할 때 참고하겠습니다.", False),
    ("publish_october_1016_1030.csv", 2, "10/23 (금) 20:00", "#8 낮잠", "october_1016_1030.md",
     "낮잠 시작할 때 틀어 두면 2시간 동안 소리가 한 번도 끊기지 않습니다 ☀️",
     "아기 낮잠이 보통 몇 분쯤에서 끝나는지 댓글로 알려 주세요.", False),
    ("publish_october_1016_1030.csv", 3, "10/27 (화) 20:00", "#9 함께 쉬는 오후", "october_1016_1030.md",
     "아기와 함께 잠깐 쉬어 가는 오후에 틀어 두세요 🌿", "", False),
    ("publish_october_1016_1030.csv", 4, "10/30 (금) 20:00", "#10 차 안", "october_1016_1030.md",
     "출발 전에 재생해 두세요 🚗 운전 중에는 화면을 조작하지 마세요.",
     "차에서 아기가 잘 자는 편인지, 자주 깨는 편인지 댓글로 알려 주세요.", False),
]

TAGS = {  # 작업서의 태그 줄
    "#4 어두운 화면": None, "#3 비 오는 밤": None, "#5 쉬 소리": None,
}


def fill(desc, prenatal):
    desc = desc.replace("[9/29 영상과 같은 검증 문구]", SAFE_PRENATAL if prenatal else SAFE_BABY)
    desc = desc.replace("00:00 [여기에 기존 '아기 수면 음악 3시간 | 무가사 피아노 자장가 14곡' 영상 설명의 수록곡·타임스탬프를 그대로 복사. 같은 음원입니다. 첫 줄은 00:00]", DARK04_SONGS)
    # "이름 — [재생목록 주소]" 줄들 → 이름 목록 + 채널 재생목록 주소 하나
    names = re.findall(r"^(.+?) — \[재생목록 주소\]$", desc, flags=re.M)
    if names:
        block = "\n".join(f"· {n}" for n in names) + f"\n\n▶ {PLAYLISTS_URL}"
        desc = re.sub(r"(^.+? — \[재생목록 주소\]\n?)+", block + "\n", desc, flags=re.M).replace(block + "\n\n", block + "\n\n", 1)
    assert "[" not in desc, desc[desc.index("["):][:80]
    return desc


def tags_from(md, title):
    text = (ROOT / "todam" / md).read_text(encoding="utf-8")
    i = text.index(title)
    m = re.search(r"태그\**\s*\n+```\n(.+?)\n```", text[i:], flags=re.S)
    return m.group(1).strip()


def main(out):
    blocks = []
    rows_by_file = {}
    for f, idx, date, label, md, pin1, pin2, prenatal in VIDEOS:
        rows = rows_by_file.setdefault(f, list(csv.DictReader(open(ROOT / "tools" / f, encoding="utf-8"))))
        r = rows[idx]
        r["description"] = fill(r["description"], prenatal)
        pin = "\n\n".join(p for p in [pin1, PIN_SAFE_PRENATAL if prenatal else PIN_SAFE_BABY, pin2] if p)
        blocks.append(f"==================== {date}  {label} ====================\n\n"
                      f"[제목]\n{r['title']}\n\n[설명]\n{r['description']}\n\n[태그]\n{tags_from(md, r['title'])}\n\n"
                      f"[고정댓글 — 공개 직후]\n{pin}\n")
    for f, rows in rows_by_file.items():
        with open(ROOT / "tools" / f, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    Path(out).write_text("\n\n".join(blocks), encoding="utf-8-sig")


if __name__ == "__main__":
    main(sys.argv[1])
