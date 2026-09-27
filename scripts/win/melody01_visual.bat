@echo off
chcp 65001 >nul
rem ============================================================
rem 동요 선율 자장가 #1 - 썸네일 3종 + 3시간 영상 합성
rem 사양: todam/visual_melody_lullaby_01.md
rem
rem 이 파일을 D:\Music\토담토담 에 복사한 뒤 더블클릭하세요.
rem 같은 폴더에 아래 파일이 있어야 합니다 (영문 파일명).
rem   bg.png          영상 배경 1920x1080 (어두운 아기방 창가, 달)
rem   mobile.png      별 모빌, 투명 배경 PNG (약 600x600)
rem   thumb_bg.png    썸네일 배경 1280x720 (오르골 + 초승달)
rem   TodamTodam_Lullaby_3Hours_Final.wav   핑크노이즈까지 넣은 최종 음원
rem   thumb_text.txt  썸네일 큰 글자 (UTF-8)
rem   thumb_sub.txt   썸네일 B형 작은 글자 (UTF-8)
rem 필요: ffmpeg (drawtext 포함된 full 빌드, 예: gyan.dev full)
rem ============================================================
setlocal
cd /d "%~dp0"
set FONT=C\:/Windows/Fonts/malgunbd.ttf

where ffmpeg >nul 2>nul || (echo ffmpeg를 찾을 수 없습니다. & pause & exit /b 1)
if not exist bg.png (echo bg.png 이 없습니다. & pause & exit /b 1)
if not exist mobile.png (echo mobile.png 이 없습니다. & pause & exit /b 1)
if not exist TodamTodam_Lullaby_3Hours_Final.wav (echo 최종 음원 WAV가 없습니다. & pause & exit /b 1)

if not exist thumb_bg.png goto video

echo [1/3] 썸네일 A 텍스트 강조형
ffmpeg -v error -y -i thumb_bg.png -vf "scale=1280:720,drawbox=x=0:y=ih*0.58:w=iw:h=ih*0.42:color=black@0.30:t=fill,drawtext=fontfile='%FONT%':textfile=thumb_text.txt:fontsize=124:fontcolor=0xFFF6E5:shadowcolor=black@0.6:shadowx=4:shadowy=4:x=80:y=h-th-90" -frames:v 1 -q:v 2 thumb_A.jpg

echo       썸네일 B 아이콘 강조형 (작은 글자)
ffmpeg -v error -y -i thumb_bg.png -vf "scale=1280:720,drawtext=fontfile='%FONT%':textfile=thumb_sub.txt:fontsize=84:fontcolor=0xFFF6E5:shadowcolor=black@0.6:shadowx=3:shadowy=3:x=80:y=h-th-90" -frames:v 1 -q:v 2 thumb_B.jpg

echo       썸네일 C 텍스트 없음
ffmpeg -v error -y -i thumb_bg.png -vf "scale=1280:720" -frames:v 1 -q:v 2 thumb_C.jpg

:video
echo [2/3] 30분 무한 반복 배경 영상 렌더 (20~40분 걸립니다)
rem 모빌: 30분에 한 바퀴 / 밝기 호흡: 60초 주기 -> 30분 끝과 처음이 정확히 이어짐
ffmpeg -v error -stats -y -loop 1 -framerate 30 -t 1800 -i bg.png -loop 1 -framerate 30 -t 1800 -i mobile.png -filter_complex "[1:v]format=rgba,rotate=a='2*PI*t/1800':c=none:ow='hypot(iw,ih)':oh=ow[mob];[0:v]scale=1920:1080,eq=brightness='0.015*sin(2*PI*t/60)':eval=frame[bgv];[bgv][mob]overlay=x='W*0.62-w/2':y='-h*0.30':format=auto,format=yuv420p[v]" -map "[v]" -c:v libx264 -preset slow -crf 28 -tune stillimage -g 300 -r 30 loop30.mp4
if errorlevel 1 (echo 배경 렌더 실패 & pause & exit /b 1)

echo [3/3] 3시간 합성 (영상은 복사만 하므로 몇 분이면 끝납니다)
ffmpeg -v error -stats -y -stream_loop -1 -i loop30.mp4 -i TodamTodam_Lullaby_3Hours_Final.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 384k -t 10800 -movflags +faststart TodamTodam_Lullaby_3Hours_Upload.mp4
if errorlevel 1 (echo 합성 실패 & pause & exit /b 1)

echo.
echo 완료: TodamTodam_Lullaby_3Hours_Upload.mp4
if exist thumb_A.jpg echo 썸네일: thumb_A.jpg 공개용 / thumb_B.jpg, thumb_C.jpg 는 7일 뒤 시험용
pause
