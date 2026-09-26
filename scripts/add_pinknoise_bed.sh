#!/usr/bin/env bash
#
# 허밍 믹스 아래에 소프트 핑크노이즈 베드를 깔고 -16 LUFS로 정리한다.
#
# 대상: 2026-09-29 공개 신규 #1 (3시간 엄마 허밍)
# 사양: plans/todam_schedule_20260923.md 10-1절, templates/audio_production_spec.md 1절
#
# 사용법:
#   ./scripts/add_pinknoise_bed.sh 허밍믹스.wav 출력.wav
#   ./scripts/add_pinknoise_bed.sh 허밍믹스.wav 출력.wav -25   # 베드를 3dB 올림
#
# 필요: ffmpeg 4.4 이상 (amix normalize 옵션)
#
set -euo pipefail

IN="${1:-}"
OUT="${2:-}"
BED_BELOW="${3:--28}"      # 허밍 대비 몇 dB 아래에 깔지. 기본 -28
LOWPASS_HZ=10000           # 이보다 위를 깎는다. 고역이 남으면 거칠게 들린다
SEED=20260929              # 고정하면 매번 같은 노이즈가 나온다

if [[ -z "$IN" || -z "$OUT" ]]; then
  sed -n "3,12p" "$0" | sed 's/^# \{0,1\}//'
  exit 1
fi
[[ -f "$IN" ]] || { echo "입력 파일이 없습니다: $IN" >&2; exit 1; }
command -v ffmpeg >/dev/null || { echo "ffmpeg가 없습니다." >&2; exit 1; }

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

# ── 통합 라우드니스를 읽는다 ─────────────────────────────
# ebur128의 마지막 Summary 블록에서 "I:" 값을 꺼낸다.
measure_lufs() {
  ffmpeg -hide_banner -nostats -i "$1" -af ebur128=peak=true -f null - 2>&1 \
    | awk '/Integrated loudness/{f=1} f && /I:/{v=$2} END{print v}'
}

echo "[1/5] 허밍 믹스 라우드니스 측정"
H="$(measure_lufs "$IN")"
[[ -n "$H" ]] || { echo "라우드니스를 읽지 못했습니다. ffmpeg 출력을 직접 확인하세요." >&2; exit 1; }
echo "      허밍 = ${H} LUFS"

# 베드 목표 = 허밍 + BED_BELOW
N_TARGET="$(awk -v h="$H" -v d="$BED_BELOW" 'BEGIN{printf "%.2f", h + d}')"
echo "      베드 목표 = ${N_TARGET} LUFS (허밍 ${BED_BELOW} dB)"

echo "[2/5] 핑크노이즈 60초 표본 생성·측정"
# 핑크노이즈는 정상 신호라 60초만 재도 전체와 같다.
ffmpeg -hide_banner -loglevel error -y \
  -f lavfi -i "anoisesrc=color=pink:sample_rate=48000:amplitude=1:seed=${SEED}:duration=60" \
  -af "lowpass=f=${LOWPASS_HZ},lowpass=f=${LOWPASS_HZ}" \
  -c:a pcm_s24le "$WORK/probe.wav"
M="$(measure_lufs "$WORK/probe.wav")"
echo "      필터 통과 후 핑크노이즈 = ${M} LUFS"

GAIN="$(awk -v n="$N_TARGET" -v m="$M" 'BEGIN{printf "%.2f", n - m}')"
echo "      적용할 게인 = ${GAIN} dB"

echo "[3/5] 믹스 (베드는 0:00부터 끝까지 연속, 페이드 없음)"
# duration=first  → 허밍 길이에서 끝난다. 노이즈는 무한 생성이므로 잘린다.
# normalize=0     → amix가 입력 개수로 나누지 않는다. 이게 없으면 허밍이 6dB 내려간다.
ffmpeg -hide_banner -loglevel error -y \
  -i "$IN" \
  -f lavfi -i "anoisesrc=color=pink:sample_rate=48000:amplitude=1:seed=${SEED}" \
  -filter_complex "\
[1:a]lowpass=f=${LOWPASS_HZ},lowpass=f=${LOWPASS_HZ},volume=${GAIN}dB,aformat=channel_layouts=stereo[bed];\
[0:a]aformat=channel_layouts=stereo[hum];\
[hum][bed]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[mix]" \
  -map "[mix]" -c:a pcm_s24le -ar 48000 "$WORK/mixed.wav"

echo "[4/5] -16 LUFS로 정리 (2패스 loudnorm)"
JSON="$(ffmpeg -hide_banner -nostats -i "$WORK/mixed.wav" \
  -af loudnorm=I=-16:TP=-1.5:LRA=4:print_format=json -f null - 2>&1 \
  | sed -n '/^{/,/^}/p')"
get() { printf '%s' "$JSON" | sed -n "s/.*\"$1\"[[:space:]]*:[[:space:]]*\"\{0,1\}\([-0-9.a-z]*\)\"\{0,1\}.*/\1/p" | head -1; }
MI="$(get input_i)"; MTP="$(get input_tp)"; MLRA="$(get input_lra)"; MTH="$(get input_thresh)"; MOFF="$(get target_offset)"
[[ -n "$MI" ]] || { echo "loudnorm 측정값을 읽지 못했습니다." >&2; exit 1; }

ffmpeg -hide_banner -loglevel error -y -i "$WORK/mixed.wav" \
  -af "loudnorm=I=-16:TP=-1.5:LRA=4:measured_I=${MI}:measured_TP=${MTP}:measured_LRA=${MLRA}:measured_thresh=${MTH}:offset=${MOFF}:linear=true" \
  -c:a pcm_s24le -ar 48000 "$OUT"

echo "[5/5] 검증"
ffmpeg -hide_banner -nostats -i "$OUT" -af ebur128=peak=true -f null - 2>&1 \
  | sed -n '/Integrated loudness/,$p'

cat <<'NOTE'

──────────────────────────────────────────
합격 기준 (templates/audio_production_spec.md 1절)

  통합 라우드니스   -16 LUFS  (허용 -17 ~ -14)
  라우드니스 레인지  4 LU 이하
  트루 피크        -1.5 dBTP 이하

기준을 벗어나면

  LRA가 4를 넘음   → 허밍 믹스 자체의 음량 변화가 큽니다. 원본에서 다이내믹을
                     줄이고 다시 돌리세요. 베드로는 해결되지 않습니다.
  베드가 너무 들림 → 세 번째 인자로 -31 정도를 주세요.
  베드가 안 들림   → -25 정도로 올리세요. 제목이 약속한 소리이므로
                     조용한 구간에서는 들려야 합니다.

귀로 확인할 곳 (가장 중요)

  0:00        노이즈가 무음에서 시작하지 않고 이미 깔려 있는지
  곡 사이     허밍이 바뀌는 지점에서 노이즈가 끊기지 않는지
  1:04:00     두 번째 순환 이음매가 노이즈에 덮여 들리는지
  2:08:00     세 번째 순환 이음매

  이어폰이 아니라 실제로 쓸 스피커로 들으세요.
──────────────────────────────────────────
NOTE
