"""편집기(db)에서 받은 사람 시각 json → 렌더용 줄 시각. 사용: python -m kids.from_editor sync/kidsNN.json (kNN.meta | -) out.json"""
import sys, json
from kids.srt import from_tap
from kids.align import parse_meta
d = json.load(open(sys.argv[1], encoding="utf-8")); d = d.get("data", d)
# meta 자리에 "-"를 주면 편집기에 저장된 줄(가사·구간 이름)을 그대로 원래 가사로 쓴다 (음원 메타 파일이 없을 때)
meta = [{"section": l.get("sec"), "text": l["text"]} for l in d["lines"] if not l.get("skip")] if sys.argv[2] == "-" else parse_meta(sys.argv[2])
res = from_tap(d, meta)
# 편집기에서 줄을 더하거나 지우면 원래 가사와 순서가 어긋나므로, 편집기에 저장된 구간 이름(sec)을 그대로 쓴다
rows = [l for l in d["lines"] if l.get("t") is not None and not l.get("skip")]
for o, r in zip(res, rows):
    if r.get("sec"): o["section"] = r["sec"]
json.dump(res, open(sys.argv[3], "w"), ensure_ascii=False)
print(len(res), "lines;", res[0]["start"], "→", res[-1]["start"])
