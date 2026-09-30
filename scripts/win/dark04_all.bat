@echo off
rem ============================================================
rem Todamtodam 10/6 #4 dark screen 3h - all in one  (guide: todam/dark04_finish.md)
rem Usage: drag the existing 3h instrumental piano file onto this bat,
rem        or put it here named muga_3h_source.<ext> and double-click.
rem Needs: ffmpeg full build (drawtext). Output: Dark04_Upload.mp4, dark04_thumb.jpg
rem Existing results are skipped. Delete a result file to rebuild it.
rem This file is ASCII-only on purpose (UTF-8 + chcp 65001 breaks cmd parsing).
rem ============================================================
setlocal
cd /d "%~dp0"
set FONT=C\:/Windows/Fonts/malgunbd.ttf
set SRC=
for %%F in (muga_3h_source.*) do set SRC=%%F
if not "%~1"=="" set "SRC=%~1"
set FINAL=Dark04_Final.wav
set UPLOAD=Dark04_Upload.mp4

where ffmpeg >nul 2>nul || (echo ERROR: ffmpeg not found. & pause & exit /b 1)
if "%SRC%"=="" (echo ERROR: no source. Drag the 3h piano file onto this bat, or name it muga_3h_source. & pause & exit /b 1)
if not exist "%SRC%" (echo ERROR: source not found: %SRC% & pause & exit /b 1)
echo Source: %SRC%

echo.
echo [1/5] Final audio - pink noise + loudness, about 10-20 min
if exist %FINAL% (echo       already exists, skipped) else (
ffmpeg -v error -stats -y -i "%SRC%" -f lavfi -i "anoisesrc=color=pink:sample_rate=48000:amplitude=1:seed=20261006" -filter_complex "[0:a]aformat=channel_layouts=stereo,acompressor=threshold=-30dB:ratio=2.5:attack=200:release=3000:makeup=1,loudnorm=I=-16:LRA=4:TP=-1.5,aresample=48000[m];[1:a]lowpass=f=10000,lowpass=f=10000,volume=-28dB,aformat=channel_layouts=stereo[bed];[m][bed]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,loudnorm=I=-16:LRA=4:TP=-1.5,aresample=48000[out]" -map "[out]" -map_metadata -1 -c:a pcm_s24le -ar 48000 -t 10800 %FINAL%
)
if not exist %FINAL% (echo ERROR: final audio failed & pause & exit /b 1)

echo.
echo [2/5] Star background and thumbnail
if not exist dark04_stars.png ffmpeg -v error -y -f lavfi -i "nullsrc=s=1920x1080:d=1,format=gray" -vf "geq=lum='if(gt(random(1),0.99955),90+random(2)*120,0)',gblur=sigma=1.2" -frames:v 1 dark04_stars.png
powershell -NoProfile -Command "[IO.File]::WriteAllText('dark04_thumb.txt', -join [char[]](0xC5B4,0xB450,0xC6B4,0x0020,0xD654,0xBA74))"
ffmpeg -v error -y -f lavfi -i "color=c=0x070A14:s=1280x720:d=1" -f lavfi -i "color=c=0xF4F1FF:s=1280x720:d=1" -i dark04_stars.png -filter_complex "[2:v]format=gray,dilation,dilation,scale=1280:720,lut=y='min(255,val*2.2)'[m];[1:v]format=rgba[w];[w][m]alphamerge[st];[0:v][st]overlay=format=auto,format=gbrp,geq=r='if(lt(hypot(X-1040,Y-200),88)*gte(hypot(X-1076,Y-176),82),245,r(X,Y))':g='if(lt(hypot(X-1040,Y-200),88)*gte(hypot(X-1076,Y-176),82),200,g(X,Y))':b='if(lt(hypot(X-1040,Y-200),88)*gte(hypot(X-1076,Y-176),82),107,b(X,Y))',format=yuv444p,drawtext=fontfile='%FONT%':textfile=dark04_thumb.txt:fontsize=132:fontcolor=0xFFF6E5:shadowcolor=black@0.7:shadowx=4:shadowy=4:x=80:y=h-th-90" -frames:v 1 -q:v 2 dark04_thumb.jpg

echo.
echo [3/5] 30-min loop background video - about 20-30 min
if exist dark04_loop30.mp4 (echo       already exists, skipped) else (
ffmpeg -v error -stats -y -loop 1 -framerate 30 -t 1800 -i dark04_stars.png -f lavfi -i "color=c=0x05070D:s=1920x1080:r=30:d=1800" -f lavfi -i "color=c=0xDDE3FF:s=1920x1080:r=30:d=1800" -filter_complex "[0:v]format=gray,split[a][b];[a][b]hstack,crop=1920:1080:x='mod(t*1920/1800,1920)':y=0[m];[2:v]format=rgba[w];[w][m]alphamerge[st];[1:v][st]overlay=format=auto,eq=brightness='0.006*sin(2*PI*t/60)':eval=frame,format=yuv420p[v]" -map "[v]" -c:v libx264 -preset slow -crf 30 -tune stillimage -g 300 -r 30 dark04_loop30.mp4
)
if not exist dark04_loop30.mp4 (echo ERROR: background video failed & pause & exit /b 1)

echo.
echo [4/5] 3-hour upload video - a few minutes
if exist %UPLOAD% (echo       already exists, skipped) else (
ffmpeg -v error -stats -y -stream_loop -1 -i dark04_loop30.mp4 -i %FINAL% -map 0:v -map 1:a -c:v copy -c:a aac -b:a 384k -t 10800 -movflags +faststart %UPLOAD%
)
if not exist %UPLOAD% (echo ERROR: upload video failed & pause & exit /b 1)

echo.
echo [5/5] Measurement - PASS: I -17..-14 LUFS, LRA 4 or less, Peak -1.5 or less, duration 10800
ffmpeg -hide_banner -nostats -i %FINAL% -af ebur128=peak=true:framelog=quiet -f null - 2>&1 | findstr /C:"I:" /C:"LRA:" /C:"Peak:"
ffprobe -v error -show_entries format=duration -of default=nw=1 %UPLOAD%

echo.
echo DONE: %UPLOAD% / thumbnail: dark04_thumb.jpg
pause
