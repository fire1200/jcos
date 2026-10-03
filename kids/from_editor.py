"""편집기(db)에서 받은 사람 시각 json → 렌더용 줄 시각. 사용: python -m kids.from_editor sync/kidsNN.json kNN.meta out.json"""
import sys, json
from kids.srt import from_tap
from kids.align import parse_meta
d = json.load(open(sys.argv[1], encoding="utf-8")); d = d.get("data", d)
res = from_tap(d, parse_meta(sys.argv[2]))
json.dump(res, open(sys.argv[3], "w"), ensure_ascii=False)
print(len(res), "lines;", res[0]["start"], "→", res[-1]["start"])
