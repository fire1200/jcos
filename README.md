# jcos

YouTube 채널 운영 계획 및 전략 문서 저장소. 현재 대상: **포근한 밤 자장가** [@dodamam](https://www.youtube.com/@dodamam) (아기 수면음악 신규 채널, 2026-09-17 [@PPAIEO](https://www.youtube.com/@PPAIEO)에서 분리 결정)

## 구성

| 경로 | 내용 |
|---|---|
| `plans/youtube_baby_sleep_exposure_v2_20260916.md` | 노출 개선 종합대책 v2. 진단 트리, 우선순위별 처방, 4주 계획, KPI |
| `plans/analysis_28d_20260819-0916.md` | @PPAIEO 28일 실측 분석. 두 장르 혼재, CTR 1.66%, 우선순위 재조정 |
| `plans/strategy_direction_20260920.md` | 다각도 재분석(수명 곡선, 노출 구간별 CTR, 길이별 유지율, 구독 전환, 업로드 밀도, 제목 패턴)과 두 채널의 전략 방향 |
| `plans/channel_split_plan_20260917.md` | 수면음악 신규 채널 분리 실행 계획. 개설 설정, 콘텐츠 이관, 8주 일정, 첫 달 목표 |
| `plans/todo_operator_20260917.md` | **운영자 실행 목록.** 채널 개설부터 4주 운영까지 메뉴 경로와 체크박스로 정리 |
| `plans/migration_ppaieo_to_dodamam_20260918.md` | **콘텐츠 이동 절차.** @PPAIEO 39편의 그룹별 처리, 영상 ID별 재업로드 순서, 일부공개 절차, 일정 |
| `plans/reupload_package_v1.md` | 새 채널 롱폼 6편 재업로드 메타데이터: 제목(한·영·일)·설명·태그·재생목록·최종화면·썸네일 문구·예약 시각 |
| `plans/album_tracklist_v1.md` | 유통용 앨범 2장(허밍·무가사 각 15곡) 트랙리스트와 원본 영상 매핑 |
| `templates/title_description_templates.md` | 제목 공식, 키워드 풀, 한·영·일 제목 샘플 20종, 설명문 템플릿 |
| `templates/thumbnail_guide.md` | 썸네일 규격·색상·시리즈별 변형·A/B 테스트 로그 |
| `templates/launch_7day_checklist.md` | 공개 전날부터 7일까지 운영 체크리스트와 배포 문안 |
| `templates/community_copy.md` | 커뮤니티 주간 루틴, 설문·팁 카드·고정댓글 문안 |
| `templates/session_design_worksheet.md` | 재생목록 구조, 최종화면 연결도, 시리즈 운영 (처방 3-2) |
| `templates/audio_production_spec.md` | 라우드니스 수치, 구간별 타임라인, 음원 출처 관리 (처방 3-4) |
| `templates/shorts_playbook.md` | 쇼츠 규격, 훅 5종 대본, 롱폼 전환 설계 (처방 3-5) |
| `templates/live_stream_runbook.md` | 24시간 라이브 송출·자동 재시작·장애 대응 (처방 3-6) |
| `templates/music_distribution_podcast_checklist.md` | YouTube Music 유통, 공식 아티스트 채널, 팟캐스트 RSS 연동 (처방 3-9) |
| `calendar/4week_calendar.xlsx` | 4주 실행 캘린더. 시작일을 바꾸면 날짜 자동 재계산 |
| `tools/kpi_tracker.xlsx` | 28일 KPI 추적 시트 + 영상별 첫 7일 로그 |
| `tools/analytics_dashboard.html` | 스튜디오 CSV 또는 직접 입력으로 노출 진단·처방을 보여주는 단일 파일 대시보드 |
| `tools/check_metadata.py` | 영상 제목·설명·시청자층·재생목록 규칙 점검 스크립트 |
| `tools/reupload_videos.csv` | 재업로드 6편 메타데이터 CSV. 점검 스크립트 통과 확인용 |
| `tools/test_check_metadata.py` | 위 점검 스크립트의 규칙 테스트 (21건) |
| `scripts/build_workbooks.py` | 위 두 xlsx 파일을 생성하는 스크립트 |

## 사용법

### 메타데이터 점검

```bash
python3 tools/check_metadata.py tools/sample_videos.csv
python3 tools/check_metadata.py my_videos.csv --format md > report.md
```

CSV 열: `title, description, made_for_kids, playlist, end_screen, duration_min`. FAIL이 하나라도 있으면 종료 코드 1.

규칙 테스트:

```bash
python3 tools/test_check_metadata.py
```

### 대시보드

`tools/analytics_dashboard.html`을 브라우저에서 열고, 스튜디오 분석 > 고급 모드 > 내보내기로 받은 CSV를 올립니다. 헤더를 보고 자동 분류하므로 어느 버튼에 올려도 됩니다. 콘텐츠 탭 "표 데이터"는 영상별 표와 노출·클릭·대량 업로드 진단에, 트래픽 소스 탭 "표 데이터"는 소스 구성에, "차트 데이터"·"총계"는 일별 추이에 쓰입니다. 외부 통신 없이 브라우저 안에서만 동작합니다. "예시 데이터 보기"로 동작을 먼저 확인할 수 있습니다.

### 엑셀 파일

노란 배경·파란 글씨 셀만 입력합니다. 수식은 파일을 열 때 자동 재계산됩니다.

```bash
pip install openpyxl
python3 scripts/build_workbooks.py   # 재생성
```
