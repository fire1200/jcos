#!/usr/bin/env bash
#
# 러닝 음원 28곡을 스트리밍 발매용으로 일괄 정리한다.
#
# 하는 일: 앞뒤 무음 제거 → 2패스 loudnorm → WAV 24bit/44.1kHz 추출 → 검증
# 사양: plans/distribution_final_20261020.md 5절
#
# 사용법:
#   ./scripts/master_for_streaming.sh 입력폴더 출력폴더
#   ./scripts/master_for_streaming.sh 입력폴더 출력폴더 -12   # 더 조용하게
#
# 필요: ffmpeg
#
set -euo pipefail

SRC="${1:-}"
DST="${2:-}"
TARGET_I="${3:--10}"     # 통합 라우드니스 목표. 스트리밍 러닝 음악은 -10 ~ -9
TARGET_TP="-1.0"         # 트루 피크
TARGET_LRA="11"          # 라우드니스 레인지. 러닝 음악은 다이내믹을 눌러도 된다
SILENCE_DB="-60dB"       # 이보다 조용하면 무음으로 본다

if [[ -z "$SRC" || -z "$DST" ]]; then
  sed -n '3,12p' "$0" | sed 's/^# \{0,1\}//'
  exit 1
fi
[[ -d "$SRC" ]] || { echo "입력 폴더가 없습니다: $SRC" >&2; exit 1; }
command -v ffmpeg >/dev/null || { echo "ffmpeg가 없습니다." >&2; exit 1; }
mkdir -p "$DST"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
REPORT="$DST/_마스터링_결과.txt"
: > "$REPORT"

measure_lufs() {
  ffmpeg -hide_banner -nostats -i "$1" -af ebur128=peak=true -f null - 2>&1 \
    | awk '/Integrated loudness/{f=1} f&&/I:/{i=$2} f&&/LRA:/{l=$2} /Peak:/{p=$2} END{print i, l, p}'
}

shopt -s nullglob nocaseglob
FILES=("$SRC"/*.{wav,flac,aiff,aif,mp3,m4a})
shopt -u nocaseglob
[[ ${#FILES[@]} -gt 0 ]] || { echo "오디오 파일이 없습니다: $SRC" >&2; exit 1; }

echo "곡 ${#FILES[@]}개를 처리합니다. 목표 ${TARGET_I} LUFS / TP ${TARGET_TP} dBTP"
echo

n=0; ok=0; warn=0
for f in "${FILES[@]}"; do
  n=$((n+1))
  base="$(basename "${f%.*}")"
  out="$DST/${base}.wav"
  printf '[%2d/%2d] %s\n' "$n" "${#FILES[@]}" "$base"

  # --- 1) 앞뒤 무음 제거 ---------------------------------------------
  # 뒤쪽은 뒤집어서 같은 필터를 한 번 더 건다.
  ffmpeg -hide_banner -loglevel error -y -i "$f" -af "\
silenceremove=start_periods=1:start_silence=0.05:start_threshold=${SILENCE_DB}:detection=peak,\
areverse,\
silenceremove=start_periods=1:start_silence=0.05:start_threshold=${SILENCE_DB}:detection=peak,\
areverse" \
    -c:a pcm_s24le -ar 44100 "$WORK/trim.wav"

  # --- 2) loudnorm 1패스 측정 ----------------------------------------
  JSON="$(ffmpeg -hide_banner -nostats -i "$WORK/trim.wav" \
    -af "loudnorm=I=${TARGET_I}:TP=${TARGET_TP}:LRA=${TARGET_LRA}:print_format=json" \
    -f null - 2>&1 | sed -n '/^{/,/^}/p')"
  get() { printf '%s' "$JSON" | sed -n "s/.*\"$1\"[[:space:]]*:[[:space:]]*\"\{0,1\}\([-0-9.a-zA-Z]*\)\"\{0,1\}.*/\1/p" | head -1; }
  MI="$(get input_i)"; MTP="$(get input_tp)"; MLRA="$(get input_lra)"
  MTH="$(get input_thresh)"; MOFF="$(get target_offset)"

  if [[ -z "$MI" || "$MI" == "-inf" ]]; then
    echo "      ⚠ 측정 실패 — 건너뜀 (무음 파일일 수 있습니다)"
    printf '%-40s 측정실패\n' "$base" >> "$REPORT"
    warn=$((warn+1)); continue
  fi

  # --- 3) loudnorm 2패스 적용 ----------------------------------------
  ffmpeg -hide_banner -loglevel error -y -i "$WORK/trim.wav" -af \
    "loudnorm=I=${TARGET_I}:TP=${TARGET_TP}:LRA=${TARGET_LRA}:measured_I=${MI}:measured_TP=${MTP}:measured_LRA=${MLRA}:measured_thresh=${MTH}:offset=${MOFF}:linear=true" \
    -c:a pcm_s24le -ar 44100 "$out"

  # --- 4) 검증 -------------------------------------------------------
  read -r FI FLRA FTP <<< "$(measure_lufs "$out")"
  flag=""
  awk -v i="$FI" -v t="$TARGET_I" 'BEGIN{exit !(i-t>1.5 || t-i>1.5)}' && flag="  ⚠ 목표에서 1.5 LU 이상 벗어남"
  printf '      이전 %6s LUFS  →  이후 %6s LUFS / LRA %5s / 피크 %6s%s\n' "$MI" "$FI" "$FLRA" "$FTP" "$flag"
  printf '%-40s %8s → %8s  LRA %6s  TP %7s%s\n' "$base" "$MI" "$FI" "$FLRA" "$FTP" "$flag" >> "$REPORT"
  [[ -z "$flag" ]] && ok=$((ok+1)) || warn=$((warn+1))
done

echo
echo "완료: 정상 ${ok}곡 / 확인 필요 ${warn}곡"
echo "결과표: $REPORT"

cat <<'NOTE'

──────────────────────────────────────────
다음에 할 일

  1. 결과표에서 ⚠ 표시된 곡을 귀로 확인하세요.
     원본이 이미 심하게 압축돼 있으면 목표에 못 맞습니다.

  2. 출력 폴더의 WAV를 그대로 유통사에 올리면 됩니다.
     24bit / 44.1kHz 입니다. DistroKid·TuneCore 모두 받습니다.

  3. 곡명은 유통사 화면에서 입력합니다. 파일명이 아닙니다.
     형식: Duiker (180 BPM)

귀로 꼭 확인할 것

  - 곡 맨 앞이 뚝 끊기며 시작하지 않는지 (무음 제거가 과했을 수 있음)
  - 곡 끝의 잔향이 잘리지 않았는지
  - 드럼이 들어오는 구간에서 찌그러지지 않는지

  무음 제거가 과하면 SILENCE_DB를 -70dB로 낮춰 다시 돌리세요.
──────────────────────────────────────────
NOTE
