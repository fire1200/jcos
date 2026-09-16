#!/usr/bin/env python3
"""영상 메타데이터 점검 스크립트 (아기 수면음악 채널).

YouTube 스튜디오 > 콘텐츠 목록을 CSV로 정리해 넣으면 제목·설명·시청자층·재생목록
규칙을 점검하고 표로 출력한다. 근거 규칙은 plans/youtube_baby_sleep_exposure_v2_20260916.md 3-1, 3-3절.

사용법:
    python3 tools/check_metadata.py tools/sample_videos.csv
    python3 tools/check_metadata.py videos.csv --format md > report.md

CSV 열 (헤더 필수, 순서 무관):
    title            제목
    description      설명 (여러 줄이면 큰따옴표로 감싸기)
    made_for_kids    yes / no
    playlist         소속 재생목록 이름 (없으면 빈칸)
    end_screen       yes / no  (최종화면 설정 여부)
    duration_min     영상 길이(분)
    tags             쉼표 구분 태그 (선택)
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass, field

CORE_KEYWORDS = [
    "아기 수면음악", "아기 잠자는 음악", "신생아 자장가", "아기 자장가",
    "아기 백색소음", "신생아 백색소음", "태교음악", "임산부 음악",
    "자궁소리", "심장박동", "아기 낮잠", "울음 멈추는", "피아노 자장가", "오르골 자장가",
    "baby sleep music", "lullaby", "white noise", "prenatal music", "womb sounds",
]
KIDS_TRIGGER_WORDS = ["키즈", "어린이", "아이들", "kids", "children", "동요", "만화", "캐릭터"]
CLICKBAIT_WORDS = ["충격", "절대", "미친", "경악", "!!!"]
LENGTH_WORDS = re.compile(r"(\d+\s*시간|\d+\s*분|\d+\s*hours?|\d+\s*min)", re.I)
NO_ADS_WORDS = ["광고없음", "광고 없음", "무광고", "no ads"]
HASHTAG = re.compile(r"#\S+")

TITLE_MAX = 60          # 검색 결과 노출 기준 안전선
KEYWORD_WINDOW = 30     # 핵심 키워드가 들어와야 하는 앞부분 글자 수
MIN_DESC_SENTENCE_CHARS = 40


@dataclass
class Result:
    title: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def status(self) -> str:
        if self.errors:
            return "FAIL"
        if self.warnings:
            return "WARN"
        return "OK"


def check_row(row: dict[str, str], seen_first_sentences: dict[str, str]) -> Result:
    title = (row.get("title") or "").strip()
    desc = (row.get("description") or "").strip()
    mfk = (row.get("made_for_kids") or "").strip().lower()
    playlist = (row.get("playlist") or "").strip()
    end_screen = (row.get("end_screen") or "").strip().lower()
    duration = (row.get("duration_min") or "").strip()
    r = Result(title=title or "(제목 없음)")

    # --- 제목 ---
    if not title:
        r.errors.append("제목 없음")
    else:
        head = title[:KEYWORD_WINDOW].lower()
        if not any(k.lower() in head for k in CORE_KEYWORDS):
            r.errors.append(f"앞 {KEYWORD_WINDOW}자 안에 핵심 키워드 없음")
        if len(title) > TITLE_MAX:
            r.warnings.append(f"제목 {len(title)}자 (권장 {TITLE_MAX}자 이하)")
        if not LENGTH_WORDS.search(title):
            r.warnings.append("제목에 길이 표기(10시간 등) 없음")
        hit = [w for w in KIDS_TRIGGER_WORDS if w.lower() in title.lower()]
        if hit:
            r.errors.append(f"아동용 자동 분류 위험 단어: {', '.join(hit)}")
        bait = [w for w in CLICKBAIT_WORDS if w in title]
        if bait:
            r.warnings.append(f"클릭베이트 표현: {', '.join(bait)}")
        if title.count("!") > 1:
            r.warnings.append("느낌표 2개 이상")
        if any(w in title.lower() for w in NO_ADS_WORDS) and duration and duration.isdigit() and int(duration) >= 480:
            r.warnings.append("'광고없음' 표기: 미드롤 광고 설정이 꺼져 있는지 확인")

    # --- 설명 ---
    if not desc:
        r.errors.append("설명 없음")
    else:
        first_line = desc.splitlines()[0].strip()
        if len(first_line) < MIN_DESC_SENTENCE_CHARS:
            r.warnings.append(f"설명 첫 줄 {len(first_line)}자, 줄글 문장으로 {MIN_DESC_SENTENCE_CHARS}자 이상 권장")
        if first_line.startswith("#") or HASHTAG.search(first_line):
            r.warnings.append("설명 첫 줄이 해시태그/키워드 나열")
        if title and not any(k.lower() in desc.lower() for k in CORE_KEYWORDS):
            r.warnings.append("설명에 핵심 키워드 없음")
        tags = HASHTAG.findall(desc)
        if len(tags) > 15:
            r.errors.append(f"해시태그 {len(tags)}개, 15개 초과 시 전부 무시됨")
        elif len(tags) > 5:
            r.warnings.append(f"해시태그 {len(tags)}개 (권장 5개 이하)")
        if "00:00" not in desc and duration and duration.isdigit() and int(duration) >= 60:
            r.warnings.append("타임스탬프(00:00) 없음")
        if not re.search(r"https?://|재생목록|playlist", desc, re.I):
            r.warnings.append("재생목록/라이브 링크 없음 (세션 연결)")
        key = first_line.lower()
        if key in seen_first_sentences:
            r.errors.append(f"설명 첫 줄이 다른 영상과 동일: '{seen_first_sentences[key][:20]}…' (비진정성 위험)")
        else:
            seen_first_sentences[key] = title

    # --- 설정 ---
    if mfk in ("yes", "y", "true", "1", "예"):
        r.errors.append("시청자층 '아동용' → 추천·알림·최종화면 제한. 부모 대상이면 '아동용 아님' 검토")
    elif mfk not in ("no", "n", "false", "0", "아니요"):
        r.warnings.append("made_for_kids 값 확인 불가 (yes/no)")
    if not playlist:
        r.warnings.append("재생목록 미배치")
    if end_screen not in ("yes", "y", "true", "1", "예"):
        r.warnings.append("최종화면 미설정")
    return r


def render_table(results: list[Result], fmt: str) -> str:
    rows = []
    for res in results:
        issues = [f"[E] {e}" for e in res.errors] + [f"[W] {w}" for w in res.warnings]
        rows.append((res.status, res.title, "; ".join(issues) or "-"))
    if fmt == "md":
        out = ["| 상태 | 제목 | 항목 |", "|---|---|---|"]
        esc = lambda x: x.replace("|", "\\|")
        out += [f"| {s} | {esc(t)} | {esc(i)} |" for s, t, i in rows]
        return "\n".join(out)
    width = max(len(t) for _, t, _ in rows) if rows else 10
    out = [f"{'상태':<5} {'제목':<{width}}  항목", "-" * (width + 60)]
    for s, t, i in rows:
        out.append(f"{s:<5} {t:<{width}}  {i}")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv_path")
    ap.add_argument("--format", choices=["text", "md"], default="text")
    args = ap.parse_args()

    with open(args.csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or "title" not in reader.fieldnames:
            print("CSV에 'title' 열이 필요합니다.", file=sys.stderr)
            return 2
        seen: dict[str, str] = {}
        results = [check_row(row, seen) for row in reader]

    print(render_table(results, args.format))
    fail = sum(r.status == "FAIL" for r in results)
    warn = sum(r.status == "WARN" for r in results)
    ok = sum(r.status == "OK" for r in results)
    print(f"\n총 {len(results)}편: OK {ok} / WARN {warn} / FAIL {fail}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
