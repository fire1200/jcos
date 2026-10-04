"""sync_tool_template.html에 세 곡의 timing.csv를 넣어 sync_tool.html을 만듭니다.

    python3 build_sync_tool.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SONGS = [("joseon_early_rap", "① 조선 전기 (1388~1592)", "조선전기"),
         ("joseon_late_rap", "② 조선 후기 (1608~1863)", "조선후기"),
         ("modern_history_rap", "③ 근현대사 (1866~1953)", "근현대사")]
data = {k: {"name": n, "file": f, "csv": open(os.path.join(HERE, k, "timing.csv"), encoding="utf-8-sig").read()}
        for k, n, f in SONGS}
tpl = open(os.path.join(HERE, "sync_tool_template.html"), encoding="utf-8").read()
out = os.path.join(HERE, "sync_tool.html")
open(out, "w", encoding="utf-8").write(tpl.replace("/*DATA*/", json.dumps(data, ensure_ascii=False)))
print(out)
