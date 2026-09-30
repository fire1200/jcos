@echo off
rem ============================================================
rem Todamtodam 10/27 #9 resting together, piano + stream 90min - all in one  (guide: todam/october_1016_1030.md section 5)
rem Put in this folder:
rem   songs\   the song files, named 01_..., 02_... in play order (any audio format)
rem   bg.png   background picture (optional - a plain gradient is used if missing)
rem   rest09_thumb.jpg  finished thumbnail (optional - if present, the thumbnail step is skipped)
rem   04_water_option_2_distant_calm_brook_10min.wav  (copy from the Suno final_wav folder)
rem Songs are played in 3 different orders, so one full cycle is 3x the song set.
rem Needs: ffmpeg full build (drawtext). Output: Rest09_Upload.mp4, rest09_thumb.jpg
rem Existing results are skipped. Delete a result file to rebuild it.
rem Changed the songs? Delete rest09_seq.wav and everything after it.
rem This file is ASCII-only on purpose (UTF-8 + chcp 65001 breaks cmd parsing).
rem ============================================================
setlocal
cd /d "%~dp0"
set FONT=C\:/Windows/Fonts/malgunbd.ttf
set ID=rest09
set DUR=5400
set FADE=60
set NOISE=none
set NOISE_DB=-28
set "TONE=anull"
set NATURE=04_water_option_2_distant_calm_brook_10min.wav
set NATURE_I=-30
set "BGEQ=eq=brightness='0.012*sin(2*PI*t/60)':eval=frame"
set FINAL=Rest09_Final.wav
set UPLOAD=Rest09_Upload.mp4
set XF=acrossfade=d=5:c1=tri:c2=tri
set /a FST=DUR-FADE
set N=0

where ffmpeg >nul 2>nul || (echo ERROR: ffmpeg not found. & pause & exit /b 1)
if not exist songs\ (echo ERROR: songs folder not found. Make a folder named songs here and put the songs in it. & pause & exit /b 1)
if not "%NATURE%"=="" if not exist "%NATURE%" (echo ERROR: nature file not found: %NATURE% & pause & exit /b 1)

echo.
echo [1/6] Prepare songs - trim silence, soft fades, even loudness, 3 play orders
if not exist %ID%_seq.wav goto doprep
echo       already exists, skipped
goto seqdone
:doprep
for %%F in (songs\*) do call :prep "%%F"
echo       %N% songs
if %N% LSS 3 (echo ERROR: need at least 3 songs in the songs folder. & pause & exit /b 1)
set /a K=N/2+1
set /a KM=K-1
set /a NM=N-1
type nul > %ID%_list.txt
for /l %%i in (1,1,%N%) do call :add %%i
for /l %%i in (%K%,1,%N%) do call :add %%i
for /l %%i in (1,1,%KM%) do call :add %%i
for /l %%i in (%NM%,-1,1) do call :add %%i
call :add %N%
ffmpeg -v error -y -f concat -safe 0 -i %ID%_list.txt -c:a pcm_s24le %ID%_seq.wav
:seqdone
if not exist %ID%_seq.wav (echo ERROR: song preparation failed & pause & exit /b 1)
if not "%NATURE%"=="" if not exist %ID%_prep_nature.wav ffmpeg -v error -y -i "%NATURE%" -t 5 -i "%NATURE%" -filter_complex "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=start=5,asetpts=PTS-STARTPTS[b];[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asetpts=PTS-STARTPTS[h];[b][h]%XF%,loudnorm=I=%NATURE_I%:TP=-6:LRA=7,aresample=48000[o]" -map "[o]" -c:a pcm_s24le %ID%_prep_nature.wav

echo.
echo [2/6] Final audio - about 10-20 min
if "%NOISE%"=="none" (set "NSRC=anullsrc=r=48000:cl=stereo") else (set "NSRC=anoisesrc=color=%NOISE%:sample_rate=48000:amplitude=1:seed=2026")
if "%NATURE%"=="" (set "NATIN=-f lavfi -i anullsrc=r=48000:cl=stereo") else (set "NATIN=-stream_loop -1 -i %ID%_prep_nature.wav")
if exist %FINAL% (echo       already exists, skipped) else (
ffmpeg -v error -stats -y -stream_loop -1 -i %ID%_seq.wav -f lavfi -i "%NSRC%" %NATIN% -filter_complex "[0:a]acompressor=threshold=-30dB:ratio=2.5:attack=200:release=3000:makeup=1,loudnorm=I=-16:LRA=4:TP=-1.5,aresample=48000[m];[1:a]lowpass=f=10000,lowpass=f=10000,volume=%NOISE_DB%dB,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[bed];[2:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[nat];[m][bed][nat]amix=inputs=3:duration=first:dropout_transition=0:normalize=0,%TONE%,loudnorm=I=-16:LRA=4:TP=-1.5,aresample=48000,afade=t=in:d=5,afade=t=out:st=%FST%:d=%FADE%[o]" -map "[o]" -t %DUR% -c:a pcm_s24le %FINAL%
)
if not exist %FINAL% (echo ERROR: final audio failed & pause & exit /b 1)

echo.
echo [3/6] 30-min loop background video - about 20-30 min
set BG=bg.png
if not exist bg.png set BG=%ID%_bg.png
if not exist %BG% ffmpeg -v error -y -f lavfi -i "gradients=s=1920x1080:c0=0xDDEBDD:c1=0xF4EFE2:x0=0:y0=0:x1=1920:y1=1080:nb_colors=2:speed=0:d=1" -vf "vignette=PI/5,format=rgb24" -frames:v 1 %ID%_bg.png
if exist %ID%_loop30.mp4 (echo       already exists, skipped) else (
ffmpeg -v error -stats -y -loop 1 -framerate 30 -t 1800 -i %BG% -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,%BGEQ%,format=yuv420p" -c:v libx264 -preset slow -crf 28 -tune stillimage -g 300 -r 30 %ID%_loop30.mp4
)
if not exist %ID%_loop30.mp4 (echo ERROR: background video failed & pause & exit /b 1)

echo.
echo [4/6] Thumbnail
if not exist %ID%_thumb.jpg goto makethumb
echo       already exists, skipped (delete %ID%_thumb.jpg to rebuild)
goto thumbdone
:makethumb
powershell -NoProfile -Command "[IO.File]::WriteAllText('%ID%_thumb.txt', -join [char[]](0xC26C,0xB294,0x0020,0xC2DC,0xAC04))"
ffmpeg -v error -y -ss 60 -i %ID%_loop30.mp4 -frames:v 1 %ID%_frame.png
ffmpeg -v error -y -i %ID%_frame.png -vf "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,eq=brightness=0.04:contrast=1.1,drawbox=x=0:y=ih*0.58:w=iw:h=ih*0.42:color=black@0.35:t=fill,drawtext=fontfile='%FONT%':textfile=%ID%_thumb.txt:fontsize=140:fontcolor=0xB8E0C8:shadowcolor=black@0.7:shadowx=4:shadowy=4:x=80:y=h-th-90" -frames:v 1 -q:v 2 %ID%_thumb.jpg
:thumbdone

echo.
echo [5/6] Upload video - a few minutes
if exist %UPLOAD% (echo       already exists, skipped) else (
ffmpeg -v error -stats -y -stream_loop -1 -i %ID%_loop30.mp4 -i %FINAL% -map 0:v -map 1:a -c:v copy -c:a aac -b:a 384k -t %DUR% -movflags +faststart %UPLOAD%
)
if not exist %UPLOAD% (echo ERROR: upload video failed & pause & exit /b 1)

echo.
echo [6/6] Measurement - PASS: I -17..-14 LUFS, LRA 4 or less, Peak -1.5 or less, duration %DUR%
ffmpeg -hide_banner -nostats -i %FINAL% -af ebur128=peak=true:framelog=quiet -f null - 2>&1 | findstr /C:"I:" /C:"LRA:" /C:"Peak:"
ffprobe -v error -show_entries format=duration -of default=nw=1 %UPLOAD%

echo.
echo DONE: %UPLOAD% / thumbnail: %ID%_thumb.jpg
pause
exit /b 0

:prep
set /a N+=1
set NN=0%N%
set NN=%NN:~-2%
echo       %NN%: %~nx1
ffmpeg -v error -y -i %1 -vn -af "aformat=sample_rates=48000:channel_layouts=stereo,silenceremove=start_periods=1:start_threshold=-55dB,areverse,silenceremove=start_periods=1:start_threshold=-55dB,afade=t=in:d=4,areverse,afade=t=in:d=1.5,loudnorm=I=-18:TP=-3:LRA=7,aresample=48000,apad=pad_dur=2" -c:a pcm_s24le %ID%_p_%NN%.wav
goto :eof

:add
set NN=0%1
set NN=%NN:~-2%
>>%ID%_list.txt echo file '%ID%_p_%NN%.wav'
goto :eof
