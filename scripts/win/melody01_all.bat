@echo off
chcp 65001 >nul
rem ============================================================
rem 동요 선율 자장가 #1 - 한 번에 끝내기
rem   1) 최종 음원: 핑크노이즈 -28dB + -16 LUFS / LRA 4 / -1.5 dBTP
rem   2) 썸네일 3종 (A 공개용, B/C 7일 뒤 시험용)
rem   3) 30분 반복 배경 영상
rem   4) 3시간 업로드 영상
rem   5) 결과 측정
rem 안내서: todam/melody_lullaby_01_finish.md
rem
rem D:\Music\토담토담 에 복사한 뒤 더블클릭. 같은 폴더에 필요한 파일:
rem   TodamTodam_Lullaby_3Hours_Suno_Master.mp3   (이미 있음)
rem   bg.png  mobile.png  thumb_bg.png  thumb_text.txt  thumb_sub.txt
rem 필요: ffmpeg full 빌드 (drawtext 포함)
rem 이미 만들어진 결과 파일은 건너뜁니다. 다시 만들려면 그 파일을 지우세요.
rem ============================================================
setlocal
cd /d "%~dp0"
set FONT=C\:/Windows/Fonts/malgunbd.ttf
set MASTER=TodamTodam_Lullaby_3Hours_Suno_Master.mp3
set FINAL=TodamTodam_Lullaby_3Hours_Final.wav
set UPLOAD=TodamTodam_Lullaby_3Hours_Upload.mp4

where ffmpeg >nul 2>nul || (echo ffmpeg를 찾을 수 없습니다. & pause & exit /b 1)
if not exist %MASTER% (echo %MASTER% 이 없습니다. & pause & exit /b 1)
if not exist bg.png (echo bg.png 이 없습니다. 안내서 3장을 보세요. & pause & exit /b 1)
if not exist mobile.png (echo mobile.png 이 없습니다. 안내서 3장을 보세요. & pause & exit /b 1)

echo.
echo [1/5] 최종 음원 - 핑크노이즈와 음량 정리, 약 10~20분
if exist %FINAL% (echo       이미 있음, 건너뜀) else (
ffmpeg -v error -stats -y -i %MASTER% -f lavfi -i "anoisesrc=color=pink:sample_rate=48000:amplitude=1:seed=20260929" -filter_complex "[0:a]aformat=channel_layouts=stereo,acompressor=threshold=-30dB:ratio=2.5:attack=200:release=3000:makeup=1,loudnorm=I=-16:LRA=4:TP=-1.5,aresample=48000[m];[1:a]lowpass=f=10000,lowpass=f=10000,volume=-28dB,aformat=channel_layouts=stereo[bed];[m][bed]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,loudnorm=I=-16:LRA=4:TP=-1.5,aresample=48000[out]" -map "[out]" -c:a pcm_s24le -ar 48000 %FINAL%
)
if not exist %FINAL% (echo 최종 음원 만들기 실패 & pause & exit /b 1)

echo.
echo [2/5] 썸네일
if not exist thumb_bg.png (echo       thumb_bg.png 없음, 건너뜀) else (
ffmpeg -v error -y -i thumb_bg.png -vf "scale=1280:720,drawbox=x=0:y=ih*0.58:w=iw:h=ih*0.42:color=black@0.30:t=fill,drawtext=fontfile='%FONT%':textfile=thumb_text.txt:fontsize=124:fontcolor=0xFFF6E5:shadowcolor=black@0.6:shadowx=4:shadowy=4:x=80:y=h-th-90" -frames:v 1 -q:v 2 thumb_A.jpg
ffmpeg -v error -y -i thumb_bg.png -vf "scale=1280:720,drawtext=fontfile='%FONT%':textfile=thumb_sub.txt:fontsize=84:fontcolor=0xFFF6E5:shadowcolor=black@0.6:shadowx=3:shadowy=3:x=80:y=h-th-90" -frames:v 1 -q:v 2 thumb_B.jpg
ffmpeg -v error -y -i thumb_bg.png -vf "scale=1280:720" -frames:v 1 -q:v 2 thumb_C.jpg
)

echo.
echo [3/5] 30분 반복 배경 영상 - 약 20~40분
if exist loop30.mp4 (echo       이미 있음, 건너뜀) else (
ffmpeg -v error -stats -y -loop 1 -framerate 30 -t 1800 -i bg.png -loop 1 -framerate 30 -t 1800 -i mobile.png -filter_complex "[1:v]format=rgba,rotate=a='2*PI*t/1800':c=none:ow='hypot(iw,ih)':oh=ow[mob];[0:v]scale=1920:1080,eq=brightness='0.015*sin(2*PI*t/60)':eval=frame[bgv];[bgv][mob]overlay=x='W*0.62-w/2':y='-h*0.30':format=auto,format=yuv420p[v]" -map "[v]" -c:v libx264 -preset slow -crf 28 -tune stillimage -g 300 -r 30 loop30.mp4
)
if not exist loop30.mp4 (echo 배경 영상 만들기 실패 & pause & exit /b 1)

echo.
echo [4/5] 3시간 업로드 영상 - 수 분
ffmpeg -v error -stats -y -stream_loop -1 -i loop30.mp4 -i %FINAL% -map 0:v -map 1:a -c:v copy -c:a aac -b:a 384k -t 10800 -movflags +faststart %UPLOAD%
if errorlevel 1 (echo 업로드 영상 만들기 실패 & pause & exit /b 1)

echo.
echo [5/5] 결과 측정 - 합격: I -17~-14 LUFS, LRA 4 이하, Peak -1.5 이하, 길이 10800초
ffmpeg -hide_banner -nostats -i %FINAL% -af ebur128=peak=true:framelog=quiet -f null - 2>&1 | findstr /C:"I:" /C:"LRA:" /C:"Peak:"
ffprobe -v error -show_entries format=duration -of default=nw=1 %UPLOAD%

echo.
echo 완료: %UPLOAD%
echo 썸네일: thumb_A.jpg 공개용 / thumb_B.jpg, thumb_C.jpg 는 7일 뒤 시험용
pause
