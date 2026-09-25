#!/usr/bin/env python3
"""check_metadata.py 규칙 테스트.

실행: python3 tools/test_check_metadata.py
"""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_metadata import check_row, render_table  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

GOOD_DESC = (
    "아기 수면음악입니다. 잠들기까지 오래 우는 신생아를 위해 엄마 심장박동 리듬과 "
    "잔잔한 피아노 자장가를 10시간 동안 끊김 없이 담았습니다.\n"
    "▶ 재생목록: https://www.youtube.com/@PPAIEO/playlists\n"
    "00:00 도입\n20:00 오르골\n#아기수면음악 #신생아자장가"
)


def row(**kw):
    base = {
        "title": "아기 수면음악 | 잠 안 자는 신생아 재우는 자장가 10시간 광고없음",
        "description": GOOD_DESC,
        "made_for_kids": "no",
        "playlist": "신생아 자장가",
        "end_screen": "yes",
        "duration_min": "600",
    }
    base.update(kw)
    return base


def issues(r, seen=None):
    res = check_row(r, {} if seen is None else seen)
    return res, res.errors + res.warnings


class TitleRules(unittest.TestCase):
    def test_clean_row_has_no_errors(self):
        res, _ = issues(row(title="아기 수면음악 | 잠 안 자는 신생아 재우는 자장가 10시간"))
        self.assertEqual(res.errors, [], res.errors)
        self.assertEqual(res.status, "OK", res.warnings)

    def test_keyword_must_be_in_first_30_chars(self):
        res, _ = issues(row(title="아주 길고 장식적인 수식어를 잔뜩 붙인 도입부가 이어지는 제목 아기 수면음악"))
        self.assertTrue(any("핵심 키워드" in e for e in res.errors))

    def test_keyword_match_ignores_spacing(self):
        res, _ = issues(row(title="아기 수면 음악 30분 | 무가사 자장가 15곡 | 신생아·영유아"))
        self.assertFalse(any("핵심 키워드" in e for e in res.errors), res.errors)

    def test_english_keyword_counts(self):
        res, _ = issues(row(title="Baby Sleep Music | 10 Hours No Ads"))
        self.assertFalse(any("핵심 키워드" in e for e in res.errors), res.errors)

    def test_kids_trigger_word_is_error(self):
        res, _ = issues(row(title="키즈 자장가 | 아기 수면음악 10시간"))
        self.assertTrue(any("아동용 자동 분류 위험" in e for e in res.errors))

    def test_missing_length_is_warning_not_error(self):
        res, _ = issues(row(title="아기 수면음악 | 잠 안 자는 신생아 재우는 자장가"))
        self.assertEqual(res.errors, [])
        self.assertTrue(any("길이 표기" in w for w in res.warnings))

    def test_clickbait_is_warning(self):
        res, _ = issues(row(title="아기 수면음악 | 충격 자장가 10시간"))
        self.assertTrue(any("클릭베이트" in w for w in res.warnings))

    def test_no_ads_claim_on_long_video_warns(self):
        res, _ = issues(row(title="아기 수면음악 | 자장가 10시간 광고없음", duration_min="600"))
        self.assertTrue(any("광고없음" in w for w in res.warnings))

    def test_no_ads_warns_on_short_video_too(self):
        """길이와 무관하게 경고한다. 유튜브는 비수익 채널 영상에도 광고를 붙일 수 있다."""
        res, _ = issues(row(title="아기 수면음악 | 자장가 60분 광고없음", duration_min="60"))
        self.assertTrue(any("광고없음" in w for w in res.warnings))

    def test_continuous_playback_wording_passes(self):
        """'연속재생'은 검증 가능한 표현이므로 경고하지 않는다."""
        res, _ = issues(row(title="아기 수면음악 | 엄마 허밍 자장가 3시간 연속재생", duration_min="180"))
        self.assertFalse(any("광고없음" in w for w in res.warnings))

    def test_no_ads_claim_on_short_video_does_not_warn(self):
        res, _ = issues(row(title="아기 수면음악 | 엄마 허밍 자장가 60분 연속재생", duration_min="60"))
        self.assertFalse(any("광고없음" in w for w in res.warnings))


class DescriptionRules(unittest.TestCase):
    def test_hashtag_over_15_is_error(self):
        desc = "아기 수면음악 설명입니다. 신생아를 위한 자장가를 담았습니다.\n" + " ".join(f"#태그{i}" for i in range(16))
        res, _ = issues(row(description=desc))
        self.assertTrue(any("15개 초과" in e for e in res.errors))

    def test_hashtag_6_to_15_is_warning(self):
        desc = "아기 수면음악 설명입니다. 신생아를 위한 자장가를 충분히 길게 담았습니다.\n재생목록\n00:00 도입\n" + " ".join(f"#태그{i}" for i in range(7))
        res, _ = issues(row(description=desc))
        self.assertEqual(res.errors, [])
        self.assertTrue(any("해시태그 7개" in w for w in res.warnings))

    def test_duplicate_first_line_across_videos_is_error(self):
        seen = {}
        first = check_row(row(title="아기 수면음악 1 | 자장가 10시간"), seen)
        second = check_row(row(title="신생아 자장가 2 | 수면음악 10시간"), seen)
        self.assertEqual(first.errors, [])
        self.assertTrue(any("동일" in e for e in second.errors))

    def test_short_first_line_warns(self):
        res, _ = issues(row(description="아기 수면음악\n00:00 도입\n재생목록"))
        self.assertTrue(any("첫 줄" in w for w in res.warnings))

    def test_timestamp_required_only_for_long_video(self):
        desc = "아기 수면음악입니다. 신생아를 위한 자장가를 길게 담은 영상입니다.\n재생목록 링크"
        long_res, _ = issues(row(description=desc, duration_min="600"))
        short_res, _ = issues(row(description=desc, duration_min="30"), seen={})
        self.assertTrue(any("타임스탬프" in w for w in long_res.warnings))
        self.assertFalse(any("타임스탬프" in w for w in short_res.warnings))


class SettingRules(unittest.TestCase):
    def test_made_for_kids_yes_is_error(self):
        res, _ = issues(row(made_for_kids="yes"))
        self.assertTrue(any("아동용" in e for e in res.errors))

    def test_korean_made_for_kids_values_accepted(self):
        res, _ = issues(row(made_for_kids="아니요"))
        self.assertFalse(any("made_for_kids" in w for w in res.warnings))

    def test_missing_playlist_and_end_screen_warn(self):
        res, _ = issues(row(playlist="", end_screen="no"))
        self.assertTrue(any("재생목록 미배치" in w for w in res.warnings))
        self.assertTrue(any("최종화면" in w for w in res.warnings))


class Rendering(unittest.TestCase):
    def test_markdown_escapes_pipe(self):
        res = check_row(row(), {})
        md = render_table([res], "md")
        body = md.splitlines()[2]
        self.assertIn("\\|", body)
        self.assertEqual(body.count("|") - body.count("\\|"), 4)

    def test_text_format_renders(self):
        out = render_table([check_row(row(), {})], "text")
        self.assertIn("상태", out)


class CommandLine(unittest.TestCase):
    def test_sample_csv_exits_nonzero_and_reports_counts(self):
        p = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "check_metadata.py"), str(ROOT / "tools" / "sample_videos.csv")],
            capture_output=True, text=True,
        )
        self.assertEqual(p.returncode, 1, p.stdout + p.stderr)
        self.assertIn("총 4편", p.stdout)

    def test_missing_title_column_exits_2(self):
        bad = ROOT / "tools" / "_tmp_bad.csv"
        bad.write_text("name,description\nx,y\n", encoding="utf-8")
        try:
            p = subprocess.run(
                [sys.executable, str(ROOT / "tools" / "check_metadata.py"), str(bad)],
                capture_output=True, text=True,
            )
            self.assertEqual(p.returncode, 2)
        finally:
            bad.unlink()


if __name__ == "__main__":
    unittest.main(verbosity=2)
