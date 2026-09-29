@echo off
chcp 65001 >nul
rem ============================================================
rem 10/9 #3 비 오는 밤 3시간 - 한 번에 끝내기
rem   빗소리 + 심장박동(자동 합성, 70 bpm) + 기존 무가사 피아노 3곡
rem 안내서: todam/rain03_finish.md
rem
rem 같은 폴더에 둘 파일 (확장자는 그대로, mp3·wav·mp4 모두 가능):
rem   rain_source.*    빗소리 5분 이상 (10분 이상 권장)
rem   piano_1.*        소담소담 빗방울 (무가사)
rem   piano_2.*        새근새근 숲속 (무가사)
rem   piano_3.*        살랑이는 모래 (무가사)
rem   화면: rain_window.* (창문 빗방울 영상, 1분 이상) 또는 rain_bg.png (그림) 중 하나
rem 필요: ffmpeg full 빌드 (drawtext 포함)
rem 결과: Rain03_Upload.mp4, rain03_thumb.jpg
rem 이미 만든 결과 파일은 건너뜁니다. 다시 만들려면 그 파일을 지우세요.
rem ============================================================
setlocal
cd /d "%~dp0"
set FONT=C\:/Windows/Fonts/malgunbd.ttf
set RAIN=
set P1=
set P2=
set P3=
set RVID=
for %%F in (rain_source.*) do set RAIN=%%F
for %%F in (piano_1.*) do set P1=%%F
for %%F in (piano_2.*) do set P2=%%F
for %%F in (piano_3.*) do set P3=%%F
for %%F in (rain_window.*) do set RVID=%%F
set FINAL=Rain03_Final.wav
set UPLOAD=Rain03_Upload.mp4
set XF=acrossfade=d=5:c1=tri:c2=tri

where ffmpeg >nul 2>nul || (echo ffmpeg를 찾을 수 없습니다. & pause & exit /b 1)
if "%RAIN%"=="" (echo rain_source 파일이 없습니다. & pause & exit /b 1)
if "%P1%"=="" (echo piano_1 파일이 없습니다. & pause & exit /b 1)
if "%P2%"=="" (echo piano_2 파일이 없습니다. & pause & exit /b 1)
if "%P3%"=="" (echo piano_3 파일이 없습니다. & pause & exit /b 1)
if "%RVID%"=="" if not exist rain_bg.png (echo 화면 소재가 없습니다. rain_window 영상 또는 rain_bg.png 를 넣으세요. & pause & exit /b 1)

echo.
echo [1/6] 소재 준비 - 빗소리·피아노 반복 이음새 정리, 심장박동 합성
if not exist rain03_prep_rain.wav ffmpeg -v error -y -i %RAIN% -t 5 -i %RAIN% -filter_complex "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=start=5,asetpts=PTS-STARTPTS[b];[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asetpts=PTS-STARTPTS[h];[b][h]%XF%,loudnorm=I=-20:TP=-3:LRA=7,aresample=48000[o]" -map "[o]" -c:a pcm_s24le rain03_prep_rain.wav
if not exist rain03_prep_heart.wav ffmpeg -v error -y -f lavfi -i "aevalsrc='(sin(2*PI*52*mod(t,60/70))*exp(-mod(t,60/70)*28)*(1-exp(-mod(t,60/70)*400))+if(gte(mod(t,60/70),0.28),0.6*sin(2*PI*46*(mod(t,60/70)-0.28))*exp(-(mod(t,60/70)-0.28)*28)*(1-exp(-(mod(t,60/70)-0.28)*400)),0))*0.8':s=48000:d=60" -af "lowpass=f=160,aformat=channel_layouts=stereo,loudnorm=I=-26:TP=-3,aresample=48000" -c:a pcm_s24le rain03_prep_heart.wav
if not exist rain03_piano_seq.wav ffmpeg -v error -y -i %P1% -i %P2% -i %P3% -filter_complex "[0:a]aformat=sample_rates=48000:channel_layouts=stereo[p0];[1:a]aformat=sample_rates=48000:channel_layouts=stereo[p1];[2:a]aformat=sample_rates=48000:channel_layouts=stereo[p2];[p0][p1]acrossfade=d=4[x];[x][p2]acrossfade=d=4[o]" -map "[o]" -c:a pcm_s24le rain03_piano_seq.wav
if not exist rain03_prep_piano.wav ffmpeg -v error -y -i rain03_piano_seq.wav -t 5 -i rain03_piano_seq.wav -filter_complex "[0:a]atrim=start=5,asetpts=PTS-STARTPTS[b];[1:a]asetpts=PTS-STARTPTS[h];[b][h]%XF%,loudnorm=I=-24:TP=-3:LRA=7,aresample=48000[o]" -map "[o]" -c:a pcm_s24le rain03_prep_piano.wav
if not exist rain03_prep_rain.wav (echo 빗소리 준비 실패 & pause & exit /b 1)
if not exist rain03_prep_piano.wav (echo 피아노 준비 실패 & pause & exit /b 1)

echo.
echo [2/6] 최종 음원 3시간 - 약 10~15분
rem 빗소리: 20분 주기로 강도가 아주 느리게 변함 / 피아노: 처음 12분 계속, 이후 20분마다 6분씩 들어왔다 나감
if exist %FINAL% (echo       이미 있음, 건너뜀) else (
ffmpeg -v error -stats -y -stream_loop -1 -i rain03_prep_rain.wav -stream_loop -1 -i rain03_prep_heart.wav -stream_loop -1 -i rain03_prep_piano.wav -filter_complex "[0:a]volume='1+0.2*sin(2*PI*t/1200)':eval=frame[r];[2:a]volume='if(lt(t,690),1,if(lt(t,720),(720-t)/30,if(lt(t,1320),0,clip(min(mod(t-1320,1200),360-mod(t-1320,1200))/30,0,1))))':eval=frame[p];[r][1:a][p]amix=inputs=3:duration=first:dropout_transition=0:normalize=0,acompressor=threshold=-30dB:ratio=2.5:attack=200:release=3000:makeup=1,loudnorm=I=-16:LRA=4:TP=-1.5,aresample=48000[o]" -map "[o]" -t 10800 -c:a pcm_s24le %FINAL%
)
if not exist %FINAL% (echo 최종 음원 만들기 실패 & pause & exit /b 1)

echo.
echo [3/6] 30분 반복 배경 영상 - 약 20~40분
if exist rain03_loop30.mp4 (echo       이미 있음, 건너뜀) else (
if not "%RVID%"=="" ffmpeg -v error -stats -y -stream_loop -1 -i %RVID% -t 1800 -an -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,eq=brightness=-0.06:saturation=0.8,fps=30,format=yuv420p" -c:v libx264 -preset medium -crf 26 -g 300 rain03_loop30.mp4
if "%RVID%"=="" ffmpeg -v error -stats -y -loop 1 -framerate 30 -t 1800 -i rain_bg.png -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,eq=brightness='0.015*sin(2*PI*t/60)':eval=frame,format=yuv420p" -c:v libx264 -preset slow -crf 28 -tune stillimage -g 300 -r 30 rain03_loop30.mp4
)
if not exist rain03_loop30.mp4 (echo 배경 영상 만들기 실패 & pause & exit /b 1)

echo.
echo [4/6] 썸네일
echo 비 오는 밤> rain03_thumb.txt
if exist rain_thumb_bg.png (set TB=rain_thumb_bg.png) else (
ffmpeg -v error -y -ss 60 -i rain03_loop30.mp4 -frames:v 1 rain03_frame.png
set TB=rain03_frame.png
)
ffmpeg -v error -y -i %TB% -vf "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,eq=brightness=0.04:contrast=1.1,drawbox=x=0:y=ih*0.58:w=iw:h=ih*0.42:color=black@0.35:t=fill,drawtext=fontfile='%FONT%':textfile=rain03_thumb.txt:fontsize=132:fontcolor=0x9FE1CB:shadowcolor=black@0.7:shadowx=4:shadowy=4:x=80:y=h-th-90" -frames:v 1 -q:v 2 rain03_thumb.jpg

echo.
echo [5/6] 3시간 업로드 영상 - 수 분
ffmpeg -v error -stats -y -stream_loop -1 -i rain03_loop30.mp4 -i %FINAL% -map 0:v -map 1:a -c:v copy -c:a aac -b:a 384k -t 10800 -movflags +faststart %UPLOAD%
if errorlevel 1 (echo 업로드 영상 만들기 실패 & pause & exit /b 1)

echo.
echo [6/6] 결과 측정 - 합격: I -17~-14 LUFS, LRA 4 이하, Peak -1.5 이하, 길이 10800초
ffmpeg -hide_banner -nostats -i %FINAL% -af ebur128=peak=true:framelog=quiet -f null - 2>&1 | findstr /C:"I:" /C:"LRA:" /C:"Peak:"
ffprobe -v error -show_entries format=duration -of default=nw=1 %UPLOAD%

echo.
echo 완료: %UPLOAD% / 썸네일: rain03_thumb.jpg
pause
