"""sync_tool_template.html에 세 곡의 timing.csv를 넣어 sync_tool.html을 만듭니다.

    python3 build_sync_tool.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SONGS = [("joseon_early_rap", "① 조선 전기 (1388~1592)", "조선전기"),
         ("joseon_late_rap", "② 조선 후기 (1608~1863)", "조선후기"),
         ("modern_history_rap", "③ 근현대사 (1866~1953)", "근현대사")]
# 링크(Artifact) 버전에 올린 싱크용 영상 주소
WEB_VIDEO = {"joseon_early_rap": "/_blob/61bdc5240ff2935162e047be45eb4fbb",
             "joseon_late_rap": "/_blob/ba6d2b107b74ba103604804bea64768b",
             "modern_history_rap": "/_blob/367452f58037b0823d2629cc86349b8c"}


def build(web):
    data = {k: {"name": n, "file": f,
                # 내려받아 쓰는 버전: 같은 폴더의 싱크용 영상을 자동으로 엶
                "video": WEB_VIDEO[k] if web else [f"싱크용_{f}.webm", f"싱크용_{f}_720p.mp4"],
                "csv": open(os.path.join(HERE, k, "timing.csv"), encoding="utf-8-sig").read()}
            for k, n, f in SONGS}
    tpl = open(os.path.join(HERE, "sync_tool_template.html"), encoding="utf-8").read()
    html = tpl.replace("/*DATA*/", json.dumps(data, ensure_ascii=False))
    if web:  # Artifact는 문서 골격을 직접 씌우므로 <title>·<style>과 본문만
        html = html[html.index("<title>"):html.index("</head>")] + html[html.index("<body>") + 6:html.index("</body>")]
    return html


open(os.path.join(HERE, "sync_tool.html"), "w", encoding="utf-8").write(build(False))
web_out = os.environ.get("WEB_OUT")
if web_out:
    open(web_out, "w", encoding="utf-8").write(build(True))
print("ok")
