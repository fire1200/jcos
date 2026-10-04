# 자막 싱크 다시 맞추기

`sync_tool.html`을 브라우저(크롬·엣지)로 열어 작업합니다. 인터넷 연결이 필요 없고, 파일은 컴퓨터 밖으로 나가지 않습니다.

1. 위쪽에서 곡을 고르고, **🎬 영상·음원 열기**로 `싱크용_*_720p.mp4`(자막 없는 영상)나 Suno mp3를 엽니다
2. 첫 줄을 클릭하고 재생 → 가사가 **시작되는 순간**마다 `Enter`
3. 어긋난 줄만 고칠 때는 그 줄을 클릭 → `←` `→`로 0.1초씩 조정, `P`로 다시 듣기
4. 노래가 쉬는 구간이 있으면 그 앞 줄에서 `E`로 끝 시각을 찍기
5. **timing.csv 저장** → 받은 파일을 보내면 영상을 다시 만듭니다

타이밍을 고치면 자막, 연도 카드, 연도 바, **장면 그림 전환까지** 함께 따라갑니다
(`timing.csv`의 `shots` 열에 줄마다 나올 그림이 적혀 있고, `make_shots.py`가 그 줄 시간 안에서 그림을 나눕니다).

## 받은 timing.csv로 다시 만들기

```bash
cp ~/받은파일/조선후기_timing.csv joseon_late_rap/timing.csv
python3 make_shots.py joseon_late_rap
cd joseon_late_rap && SONG_DIR=. python3 ../modern_history_rap/render.py
python3 ../make_srt.py && python3 ../build_sync_tool.py
```

| 파일 | 내용 |
|---|---|
| `sync_tool_template.html` | 싱크 도구 원본 |
| `build_sync_tool.py` | 세 곡의 timing.csv를 넣어 `sync_tool.html`을 만듦 |
| `make_shots.py` | timing.csv의 `shots` 열로 그림 전환표(shots.csv) 생성 (세 곡 공용) |
| `make_srt.py` | timing.csv로 유튜브 자막 .srt 생성 |
| `modern_history_rap/render.py` | 영상 생성기. `CLEAN=1`이면 자막 없는 싱크용 영상 |
