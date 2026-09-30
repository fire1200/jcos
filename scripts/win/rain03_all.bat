@echo off
rem ============================================================
rem Todamtodam 10/9 #3 rainy night 3h - all in one  (guide: todam/rain03_finish.md)
rem Put in this folder: rain_source.<ext> (or 01_rain_option_1_window_night_10min.wav),
rem   piano_1/2/3.<ext>, and rain_bg.png (or rain_window.<ext> video). Then double-click.
rem Heartbeat (70 bpm) is synthesized automatically.
rem Needs: ffmpeg full build (drawtext). Output: Rain03_Upload.mp4, rain03_thumb.jpg
rem Existing results are skipped. Delete a result file to rebuild it.
rem This file is ASCII-only on purpose (UTF-8 + chcp 65001 breaks cmd parsing).
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
if "%RAIN%"=="" if exist 01_rain_option_1_window_night_10min.wav set RAIN=01_rain_option_1_window_night_10min.wav
for %%F in (piano_1.*) do set P1=%%F
for %%F in (piano_2.*) do set P2=%%F
for %%F in (piano_3.*) do set P3=%%F
for %%F in (rain_window.*) do set RVID=%%F
set FINAL=Rain03_Final.wav
set UPLOAD=Rain03_Upload.mp4
set XF=acrossfade=d=5:c1=tri:c2=tri

where ffmpeg >nul 2>nul || (echo ERROR: ffmpeg not found. & pause & exit /b 1)
if "%RAIN%"=="" (echo ERROR: rain_source file not found. & pause & exit /b 1)
if "%P1%"=="" (echo ERROR: piano_1 file not found. & pause & exit /b 1)
if "%P2%"=="" (echo ERROR: piano_2 file not found. & pause & exit /b 1)
if "%P3%"=="" (echo ERROR: piano_3 file not found. & pause & exit /b 1)
if "%RVID%"=="" if not exist rain_bg.png (echo ERROR: no visual. Put rain_bg.png or a rain_window video here. & pause & exit /b 1)

echo.
echo [1/6] Prepare sources - rain/piano seamless loops, heartbeat synthesis
if not exist rain03_prep_rain.wav ffmpeg -v error -y -i "%RAIN%" -t 5 -i "%RAIN%" -filter_complex "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=start=5,asetpts=PTS-STARTPTS[b];[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asetpts=PTS-STARTPTS[h];[b][h]%XF%,loudnorm=I=-20:TP=-3:LRA=7,aresample=48000[o]" -map "[o]" -c:a pcm_s24le rain03_prep_rain.wav
if not exist rain03_prep_heart.wav ffmpeg -v error -y -f lavfi -i "aevalsrc='(sin(2*PI*52*mod(t,60/70))*exp(-mod(t,60/70)*28)*(1-exp(-mod(t,60/70)*400))+if(gte(mod(t,60/70),0.28),0.6*sin(2*PI*46*(mod(t,60/70)-0.28))*exp(-(mod(t,60/70)-0.28)*28)*(1-exp(-(mod(t,60/70)-0.28)*400)),0))*0.8':s=48000:d=60" -af "lowpass=f=160,aformat=channel_layouts=stereo,loudnorm=I=-26:TP=-3,aresample=48000" -c:a pcm_s24le rain03_prep_heart.wav
if not exist rain03_piano_seq.wav ffmpeg -v error -y -i "%P1%" -i "%P2%" -i "%P3%" -filter_complex "[0:a]aformat=sample_rates=48000:channel_layouts=stereo[p0];[1:a]aformat=sample_rates=48000:channel_layouts=stereo[p1];[2:a]aformat=sample_rates=48000:channel_layouts=stereo[p2];[p0][p1]acrossfade=d=4[x];[x][p2]acrossfade=d=4[o]" -map "[o]" -c:a pcm_s24le rain03_piano_seq.wav
if not exist rain03_prep_piano.wav ffmpeg -v error -y -i rain03_piano_seq.wav -t 5 -i rain03_piano_seq.wav -filter_complex "[0:a]atrim=start=5,asetpts=PTS-STARTPTS[b];[1:a]asetpts=PTS-STARTPTS[h];[b][h]%XF%,loudnorm=I=-24:TP=-3:LRA=7,aresample=48000[o]" -map "[o]" -c:a pcm_s24le rain03_prep_piano.wav
if not exist rain03_prep_rain.wav (echo ERROR: rain prep failed & pause & exit /b 1)
if not exist rain03_prep_piano.wav (echo ERROR: piano prep failed & pause & exit /b 1)

echo.
echo [2/6] Final 3-hour audio - about 10-15 min
if exist %FINAL% (echo       already exists, skipped) else (
ffmpeg -v error -stats -y -stream_loop -1 -i rain03_prep_rain.wav -stream_loop -1 -i rain03_prep_heart.wav -stream_loop -1 -i rain03_prep_piano.wav -filter_complex "[0:a]volume='1+0.2*sin(2*PI*t/1200)':eval=frame[r];[2:a]volume='if(lt(t,690),1,if(lt(t,720),(720-t)/30,if(lt(t,1320),0,clip(min(mod(t-1320,1200),360-mod(t-1320,1200))/30,0,1))))':eval=frame[p];[r][1:a][p]amix=inputs=3:duration=first:dropout_transition=0:normalize=0,acompressor=threshold=-30dB:ratio=2.5:attack=200:release=3000:makeup=1,loudnorm=I=-16:LRA=4:TP=-1.5,aresample=48000[o]" -map "[o]" -t 10800 -c:a pcm_s24le %FINAL%
)
if not exist %FINAL% (echo ERROR: final audio failed & pause & exit /b 1)

echo.
echo [3/6] 30-min loop background video - about 20-40 min
if exist rain03_loop30.mp4 (echo       already exists, skipped) else (
if not "%RVID%"=="" ffmpeg -v error -stats -y -stream_loop -1 -i "%RVID%" -t 1800 -an -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,eq=brightness=-0.06:saturation=0.8,fps=30,format=yuv420p" -c:v libx264 -preset medium -crf 26 -g 300 rain03_loop30.mp4
if "%RVID%"=="" ffmpeg -v error -stats -y -loop 1 -framerate 30 -t 1800 -i rain_bg.png -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,eq=brightness='0.015*sin(2*PI*t/60)':eval=frame,format=yuv420p" -c:v libx264 -preset slow -crf 28 -tune stillimage -g 300 -r 30 rain03_loop30.mp4
)
if not exist rain03_loop30.mp4 (echo ERROR: background video failed & pause & exit /b 1)

echo.
echo [4/6] Thumbnail
powershell -NoProfile -Command "[IO.File]::WriteAllText('rain03_thumb.txt', -join [char[]](0xBE44,0x0020,0xC624,0xB294,0x0020,0xBC24))"
if exist rain_thumb_bg.png (set TB=rain_thumb_bg.png) else (
ffmpeg -v error -y -ss 60 -i rain03_loop30.mp4 -frames:v 1 rain03_frame.png
set TB=rain03_frame.png
)
ffmpeg -v error -y -i %TB% -vf "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,eq=brightness=0.04:contrast=1.1,drawbox=x=0:y=ih*0.58:w=iw:h=ih*0.42:color=black@0.35:t=fill,drawtext=fontfile='%FONT%':textfile=rain03_thumb.txt:fontsize=132:fontcolor=0x9FE1CB:shadowcolor=black@0.7:shadowx=4:shadowy=4:x=80:y=h-th-90" -frames:v 1 -q:v 2 rain03_thumb.jpg

echo.
echo [5/6] 3-hour upload video - a few minutes
if exist %UPLOAD% (echo       already exists, skipped) else (
ffmpeg -v error -stats -y -stream_loop -1 -i rain03_loop30.mp4 -i %FINAL% -map 0:v -map 1:a -c:v copy -c:a aac -b:a 384k -t 10800 -movflags +faststart %UPLOAD%
)
if not exist %UPLOAD% (echo ERROR: upload video failed & pause & exit /b 1)

echo.
echo [6/6] Measurement - PASS: I -17..-14 LUFS, LRA 4 or less, Peak -1.5 or less, duration 10800
ffmpeg -hide_banner -nostats -i %FINAL% -af ebur128=peak=true:framelog=quiet -f null - 2>&1 | findstr /C:"I:" /C:"LRA:" /C:"Peak:"
ffprobe -v error -show_entries format=duration -of default=nw=1 %UPLOAD%

echo.
echo DONE: %UPLOAD% / thumbnail: rain03_thumb.jpg
pause
