"""각 곡의 shots_chatgpt.md에서 ChatGPT에 그대로 붙여 넣을 의뢰 메시지 묶음을 만듭니다.

    python3 make_chatgpt_requests.py prehistory_song samguk_rise_song ...   # out/ChatGPT_의뢰_<곡>.md

메시지 하나 = 사건 하나(그림 3장)라서, 붙여 넣기 한 번에 a·b·c 세 장을 받습니다.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("OUT", os.path.join(HERE, "out"))
NAMES = {"prehistory_song": ("⓪", "선사 시대", "선사시대"),
         "samguk_rise_song": ("①", "고조선과 삼국", "고조선삼국"),
         "samguk_war_song": ("②", "삼국 통일 전쟁", "삼국통일"),
         "nambukguk_song": ("③", "남북국 시대", "남북국")}


def parse(song):
    s = open(os.path.join(HERE, song, "shots_chatgpt.md"), encoding="utf-8").read()
    rules = re.search(r"## 1\..*?```\n(.*?)```", s, re.S).group(1).strip()
    events = []
    for m in re.finditer(r"### (\d\d) (.+?)\n(.*?)(?=\n### \d\d |\n---)", s, re.S):
        num, title, body = m.groups()
        note = re.search(r"> \*\*고증 핵심\*\*: (.+)", body)
        shots = re.findall(r"\*\*(\d\d[abc]) — (.+?)\*\*\n```\n(.*?)```", body, re.S)
        events.append((num, title, note.group(1) if note else "", shots))
    return rules, events


def build(song):
    mark, name, tag = NAMES.get(song, ("", song, song))
    rules, events = parse(song)
    n = sum(len(e[3]) for e in events)
    out = [f"# {mark} {name} — ChatGPT 그림 의뢰 메시지 ({n}장)\n",
           "**쓰는 법**",
           "1. ChatGPT에서 **새 대화**를 엽니다.",
           "2. 아래 **메시지 0**(공통 규칙)을 그대로 붙여 넣어 보냅니다.",
           f"3. **메시지 01**부터 차례로 하나씩 붙여 넣습니다. 메시지 하나에 그림 3장(a·b·c)입니다.",
           "4. 받은 그림을 메시지에 적힌 파일 이름(예: `01a.png`)으로 저장합니다.",
           f"5. 몇 개씩 모아 압축해서 올려 주세요. 압축 파일 이름에 넣을 말: **{tag}**\n",
           "> ChatGPT가 한 번에 한 장만 그리면 \"다음 장 그려 줘\"라고 보내면 이어서 그립니다.\n",
           "---\n", "## 메시지 0 — 공통 규칙 (맨 처음 한 번)\n", "```", rules, "```\n"]
    for num, title, note, shots in events:
        out += ["---\n", f"## 메시지 {num} — {title}\n", "```",
                f"[{tag} {num}] {title}",
                f"고증 핵심: {note}" if note else "",
                "",
                "아래 장면을 한 장씩 차례로 그려 줘. 공통 규칙(화풍, 고증, 가로 1536×1024, 글자 없음, 얼굴 정면 금지)을 꼭 지키고,",
                "그림을 줄 때마다 답장 글 첫 줄에 파일 이름을 적어 줘. 그림 안에는 글자를 넣지 마.",
                ""]
        for fid, kind, prompt in shots:
            out += [f"■ {fid}.png ({kind})", " ".join(prompt.split()), ""]
        out += ["```\n"]
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"ChatGPT_의뢰_{mark}_{name.replace(' ', '')}.md")
    open(path, "w", encoding="utf-8").write("\n".join(l for l in out if l is not None))
    print(path, len(events), "메시지", n, "장")
    return path


if __name__ == "__main__":
    for s in sys.argv[1:] or list(NAMES):
        build(s)
