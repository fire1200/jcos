@echo off
rem ============================================================
rem Todamtodam 10/13 #5 shush + rain + stream 3h - all in one  (guide: todam/shush05_finish.md)
rem Put this bat in D:\Music\...\suno_1001_1120\final_wav and copy rain_bg.png there.
rem Uses the Suno files below by name. Change the set lines to use other options.
rem Optional: hum_source.<ext> adds very quiet humming.
rem Needs: ffmpeg full build (drawtext). Output: Shush05_Upload.mp4, shush05_thumb.jpg
rem Existing results are skipped. Delete a result file to rebuild it.
rem This file is ASCII-only on purpose (UTF-8 + chcp 65001 breaks cmd parsing).
rem ============================================================
setlocal
cd /d "%~dp0"
set FONT=C\:/Windows/Fonts/malgunbd.ttf
set SHUSH=05_shush_option_1_continuous_soft_10min.wav
set RAIN=02_rain_option_2_warm_roof_window_10min.wav
set WATER=03_water_option_1_small_stream_stones_10min.wav
set HUM=
for %%F in (hum_source.*) do set HUM=%%F
set FINAL=Shush05_Final.wav
set UPLOAD=Shush05_Upload.mp4
set XF=acrossfade=d=5:c1=tri:c2=tri

where ffmpeg >nul 2>nul || (echo ERROR: ffmpeg not found. & pause & exit /b 1)
if not exist "%SHUSH%" (echo ERROR: shush file not found: %SHUSH% & pause & exit /b 1)
if not exist "%RAIN%" (echo ERROR: rain file not found: %RAIN% & pause & exit /b 1)
if not exist "%WATER%" (echo ERROR: water file not found: %WATER% & pause & exit /b 1)
if not exist rain_bg.png (echo ERROR: rain_bg.png not found. Copy it from the #3 prep folder. & pause & exit /b 1)

echo.
echo [1/6] Prepare sources - seamless loops, level matching
if not exist shush05_prep_shush.wav ffmpeg -v error -y -i "%SHUSH%" -t 5 -i "%SHUSH%" -filter_complex "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=start=5,asetpts=PTS-STARTPTS[b];[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asetpts=PTS-STARTPTS[h];[b][h]%XF%,loudnorm=I=-20:TP=-3:LRA=7,aresample=48000[o]" -map "[o]" -c:a pcm_s24le shush05_prep_shush.wav
if not exist shush05_prep_rain.wav ffmpeg -v error -y -i "%RAIN%" -t 5 -i "%RAIN%" -filter_complex "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=start=5,asetpts=PTS-STARTPTS[b];[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asetpts=PTS-STARTPTS[h];[b][h]%XF%,loudnorm=I=-20:TP=-3:LRA=7,aresample=48000[o]" -map "[o]" -c:a pcm_s24le shush05_prep_rain.wav
if not exist shush05_prep_water.wav ffmpeg -v error -y -i "%WATER%" -t 5 -i "%WATER%" -filter_complex "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=start=5,asetpts=PTS-STARTPTS[b];[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asetpts=PTS-STARTPTS[h];[b][h]%XF%,loudnorm=I=-23:TP=-3:LRA=7,aresample=48000[o]" -map "[o]" -c:a pcm_s24le shush05_prep_water.wav
if not "%HUM%"=="" if not exist shush05_prep_hum.wav ffmpeg -v error -y -i "%HUM%" -t 5 -i "%HUM%" -filter_complex "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=start=5,asetpts=PTS-STARTPTS[b];[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asetpts=PTS-STARTPTS[h];[b][h]%XF%,loudnorm=I=-30:TP=-6:LRA=7,aresample=48000[o]" -map "[o]" -c:a pcm_s24le shush05_prep_hum.wav
if not exist shush05_prep_water.wav (echo ERROR: source prep failed & pause & exit /b 1)

echo.
echo [2/6] Final 3-hour audio - about 10-15 min
if exist %FINAL% (echo       already exists, skipped) else (
if "%HUM%"=="" ffmpeg -v error -stats -y -stream_loop -1 -i shush05_prep_shush.wav -stream_loop -1 -i shush05_prep_rain.wav -stream_loop -1 -i shush05_prep_water.wav -filter_complex "[0:a]volume='if(lt(t,240),1,1+0.25*sin(2*PI*(t-240)/1200))':eval=frame[s];[1:a]volume='if(lt(t,180),0,if(lt(t,240),(t-180)/60,1-0.25*sin(2*PI*(t-240)/1200)))':eval=frame[r];[2:a]volume='if(lt(t,600),0,if(lt(t,660),(t-600)/60,1+0.2*sin(2*PI*(t-660)/1200)))':eval=frame[w];[s][r][w]amix=inputs=3:duration=first:dropout_transition=0:normalize=0,acompressor=threshold=-30dB:ratio=2.5:attack=200:release=3000:makeup=1,loudnorm=I=-16:LRA=4:TP=-1.5,aresample=48000[o]" -map "[o]" -t 10800 -c:a pcm_s24le %FINAL%
if not "%HUM%"=="" ffmpeg -v error -stats -y -stream_loop -1 -i shush05_prep_shush.wav -stream_loop -1 -i shush05_prep_rain.wav -stream_loop -1 -i shush05_prep_water.wav -stream_loop -1 -i shush05_prep_hum.wav -filter_complex "[0:a]volume='if(lt(t,240),1,1+0.25*sin(2*PI*(t-240)/1200))':eval=frame[s];[1:a]volume='if(lt(t,180),0,if(lt(t,240),(t-180)/60,1-0.25*sin(2*PI*(t-240)/1200)))':eval=frame[r];[2:a]volume='if(lt(t,600),0,if(lt(t,660),(t-600)/60,1+0.2*sin(2*PI*(t-660)/1200)))':eval=frame[w];[s][r][w][3:a]amix=inputs=4:duration=first:dropout_transition=0:normalize=0,acompressor=threshold=-30dB:ratio=2.5:attack=200:release=3000:makeup=1,loudnorm=I=-16:LRA=4:TP=-1.5,aresample=48000[o]" -map "[o]" -t 10800 -c:a pcm_s24le %FINAL%
)
if not exist %FINAL% (echo ERROR: final audio failed & pause & exit /b 1)

echo.
echo [3/6] 30-min loop background video, bluer tone - about 20-30 min
if exist shush05_loop30.mp4 (echo       already exists, skipped) else (
ffmpeg -v error -stats -y -loop 1 -framerate 30 -t 1800 -i rain_bg.png -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,colorbalance=rs=-0.06:bs=0.08:rm=-0.04:bm=0.06,eq=brightness='-0.03+0.015*sin(2*PI*t/60)':eval=frame,format=yuv420p" -c:v libx264 -preset slow -crf 28 -tune stillimage -g 300 -r 30 shush05_loop30.mp4
)
if not exist shush05_loop30.mp4 (echo ERROR: background video failed & pause & exit /b 1)

echo.
echo [4/6] Thumbnail
powershell -NoProfile -Command "[IO.File]::WriteAllText('shush05_thumb.txt', -join [char[]](0xC26C,0x0020,0xC18C,0xB9AC))"
ffmpeg -v error -y -ss 60 -i shush05_loop30.mp4 -frames:v 1 shush05_frame.png
ffmpeg -v error -y -i shush05_frame.png -vf "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,eq=brightness=0.05:contrast=1.1,drawbox=x=0:y=ih*0.58:w=iw:h=ih*0.42:color=black@0.35:t=fill,drawtext=fontfile='%FONT%':textfile=shush05_thumb.txt:fontsize=140:fontcolor=0x9FE1CB:shadowcolor=black@0.7:shadowx=4:shadowy=4:x=80:y=h-th-90" -frames:v 1 -q:v 2 shush05_thumb.jpg

echo.
echo [5/6] 3-hour upload video - a few minutes
if exist %UPLOAD% (echo       already exists, skipped) else (
ffmpeg -v error -stats -y -stream_loop -1 -i shush05_loop30.mp4 -i %FINAL% -map 0:v -map 1:a -c:v copy -c:a aac -b:a 384k -t 10800 -movflags +faststart %UPLOAD%
)
if not exist %UPLOAD% (echo ERROR: upload video failed & pause & exit /b 1)

echo.
echo [6/6] Measurement - PASS: I -17..-14 LUFS, LRA 4 or less, Peak -1.5 or less, duration 10800
ffmpeg -hide_banner -nostats -i %FINAL% -af ebur128=peak=true:framelog=quiet -f null - 2>&1 | findstr /C:"I:" /C:"LRA:" /C:"Peak:"
ffprobe -v error -show_entries format=duration -of default=nw=1 %UPLOAD%

echo.
echo DONE: %UPLOAD% / thumbnail: shush05_thumb.jpg
pause
