@echo off
chcp 65001 >nul
rem ============================================================
rem 10/13 #5 쉬 소리 + 빗소리 + 물소리 3시간 - 한 번에 끝내기
rem 안내서: todam/shush05_finish.md
rem
rem 이 파일을 D:\Music\토담토담\suno_1001_1120\final_wav 에 넣고 더블클릭하세요.
rem 그 폴더의 아래 파일을 그대로 씁니다 (이름 변경 불필요):
rem   05_shush_option_1_continuous_soft_10min.wav   쉬 소리 (1안, 끊김 없는)
rem   02_rain_option_2_warm_roof_window_10min.wav   빗소리 (2안 - 10/9 #3은 1안이라 겹치지 않게)
rem   03_water_option_1_small_stream_stones_10min.wav 물소리 (1안)
rem 같은 폴더에 rain_bg.png 를 복사해 두세요 (#3과 같은 그림, 더 푸르게 바꿔 씀).
rem 선택: hum_source.* 가 있으면 엄마 허밍을 아주 낮게(10%) 깔아 줍니다.
rem 다른 안을 쓰려면 아래 set 줄의 파일 이름만 바꾸세요.
rem 필요: ffmpeg full 빌드 (drawtext 포함)
rem 결과: Shush05_Upload.mp4, shush05_thumb.jpg
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

where ffmpeg >nul 2>nul || (echo ffmpeg를 찾을 수 없습니다. & pause & exit /b 1)
if not exist "%SHUSH%" (echo 쉬 소리 파일이 없습니다: %SHUSH% & pause & exit /b 1)
if not exist "%RAIN%" (echo 빗소리 파일이 없습니다: %RAIN% & pause & exit /b 1)
if not exist "%WATER%" (echo 물소리 파일이 없습니다: %WATER% & pause & exit /b 1)
if not exist rain_bg.png (echo rain_bg.png 이 없습니다. #3 준비 폴더에서 복사하세요. & pause & exit /b 1)

echo.
echo [1/6] 소재 준비 - 반복 이음새 정리, 소리별 음량 맞춤
if not exist shush05_prep_shush.wav ffmpeg -v error -y -i "%SHUSH%" -t 5 -i "%SHUSH%" -filter_complex "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=start=5,asetpts=PTS-STARTPTS[b];[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asetpts=PTS-STARTPTS[h];[b][h]%XF%,loudnorm=I=-20:TP=-3:LRA=7,aresample=48000[o]" -map "[o]" -c:a pcm_s24le shush05_prep_shush.wav
if not exist shush05_prep_rain.wav ffmpeg -v error -y -i "%RAIN%" -t 5 -i "%RAIN%" -filter_complex "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=start=5,asetpts=PTS-STARTPTS[b];[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asetpts=PTS-STARTPTS[h];[b][h]%XF%,loudnorm=I=-20:TP=-3:LRA=7,aresample=48000[o]" -map "[o]" -c:a pcm_s24le shush05_prep_rain.wav
if not exist shush05_prep_water.wav ffmpeg -v error -y -i "%WATER%" -t 5 -i "%WATER%" -filter_complex "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=start=5,asetpts=PTS-STARTPTS[b];[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asetpts=PTS-STARTPTS[h];[b][h]%XF%,loudnorm=I=-23:TP=-3:LRA=7,aresample=48000[o]" -map "[o]" -c:a pcm_s24le shush05_prep_water.wav
if not "%HUM%"=="" if not exist shush05_prep_hum.wav ffmpeg -v error -y -i "%HUM%" -t 5 -i "%HUM%" -filter_complex "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=start=5,asetpts=PTS-STARTPTS[b];[1:a]aformat=sample_rates=48000:channel_layouts=stereo,asetpts=PTS-STARTPTS[h];[b][h]%XF%,loudnorm=I=-30:TP=-6:LRA=7,aresample=48000[o]" -map "[o]" -c:a pcm_s24le shush05_prep_hum.wav
if not exist shush05_prep_water.wav (echo 소재 준비 실패 & pause & exit /b 1)

echo.
echo [2/6] 최종 음원 3시간 - 약 10~15분
rem 0~3분 쉬 소리만 / 3~4분 빗소리 합류 / 10~11분 물소리 합류 / 이후 20분 주기로 세 소리 비율이 완만히 교대
if exist %FINAL% (echo       이미 있음, 건너뜀) else (
if "%HUM%"=="" ffmpeg -v error -stats -y -stream_loop -1 -i shush05_prep_shush.wav -stream_loop -1 -i shush05_prep_rain.wav -stream_loop -1 -i shush05_prep_water.wav -filter_complex "[0:a]volume='if(lt(t,240),1,1+0.25*sin(2*PI*(t-240)/1200))':eval=frame[s];[1:a]volume='if(lt(t,180),0,if(lt(t,240),(t-180)/60,1-0.25*sin(2*PI*(t-240)/1200)))':eval=frame[r];[2:a]volume='if(lt(t,600),0,if(lt(t,660),(t-600)/60,1+0.2*sin(2*PI*(t-660)/1200)))':eval=frame[w];[s][r][w]amix=inputs=3:duration=first:dropout_transition=0:normalize=0,acompressor=threshold=-30dB:ratio=2.5:attack=200:release=3000:makeup=1,loudnorm=I=-16:LRA=4:TP=-1.5,aresample=48000[o]" -map "[o]" -t 10800 -c:a pcm_s24le %FINAL%
if not "%HUM%"=="" ffmpeg -v error -stats -y -stream_loop -1 -i shush05_prep_shush.wav -stream_loop -1 -i shush05_prep_rain.wav -stream_loop -1 -i shush05_prep_water.wav -stream_loop -1 -i shush05_prep_hum.wav -filter_complex "[0:a]volume='if(lt(t,240),1,1+0.25*sin(2*PI*(t-240)/1200))':eval=frame[s];[1:a]volume='if(lt(t,180),0,if(lt(t,240),(t-180)/60,1-0.25*sin(2*PI*(t-240)/1200)))':eval=frame[r];[2:a]volume='if(lt(t,600),0,if(lt(t,660),(t-600)/60,1+0.2*sin(2*PI*(t-660)/1200)))':eval=frame[w];[s][r][w][3:a]amix=inputs=4:duration=first:dropout_transition=0:normalize=0,acompressor=threshold=-30dB:ratio=2.5:attack=200:release=3000:makeup=1,loudnorm=I=-16:LRA=4:TP=-1.5,aresample=48000[o]" -map "[o]" -t 10800 -c:a pcm_s24le %FINAL%
)
if not exist %FINAL% (echo 최종 음원 만들기 실패 & pause & exit /b 1)

echo.
echo [3/6] 30분 반복 배경 영상 (더 푸른 색) - 약 20~30분
if exist shush05_loop30.mp4 (echo       이미 있음, 건너뜀) else (
ffmpeg -v error -stats -y -loop 1 -framerate 30 -t 1800 -i rain_bg.png -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,colorbalance=rs=-0.06:bs=0.08:rm=-0.04:bm=0.06,eq=brightness='-0.03+0.015*sin(2*PI*t/60)':eval=frame,format=yuv420p" -c:v libx264 -preset slow -crf 28 -tune stillimage -g 300 -r 30 shush05_loop30.mp4
)
if not exist shush05_loop30.mp4 (echo 배경 영상 만들기 실패 & pause & exit /b 1)

echo.
echo [4/6] 썸네일
echo 쉬 소리> shush05_thumb.txt
ffmpeg -v error -y -ss 60 -i shush05_loop30.mp4 -frames:v 1 shush05_frame.png
ffmpeg -v error -y -i shush05_frame.png -vf "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,eq=brightness=0.05:contrast=1.1,drawbox=x=0:y=ih*0.58:w=iw:h=ih*0.42:color=black@0.35:t=fill,drawtext=fontfile='%FONT%':textfile=shush05_thumb.txt:fontsize=140:fontcolor=0x9FE1CB:shadowcolor=black@0.7:shadowx=4:shadowy=4:x=80:y=h-th-90" -frames:v 1 -q:v 2 shush05_thumb.jpg

echo.
echo [5/6] 3시간 업로드 영상 - 수 분
ffmpeg -v error -stats -y -stream_loop -1 -i shush05_loop30.mp4 -i %FINAL% -map 0:v -map 1:a -c:v copy -c:a aac -b:a 384k -t 10800 -movflags +faststart %UPLOAD%
if errorlevel 1 (echo 업로드 영상 만들기 실패 & pause & exit /b 1)

echo.
echo [6/6] 결과 측정 - 합격: I -17~-14 LUFS, LRA 4 이하, Peak -1.5 이하, 길이 10800초
ffmpeg -hide_banner -nostats -i %FINAL% -af ebur128=peak=true:framelog=quiet -f null - 2>&1 | findstr /C:"I:" /C:"LRA:" /C:"Peak:"
ffprobe -v error -show_entries format=duration -of default=nw=1 %UPLOAD%

echo.
echo 완료: %UPLOAD% / 썸네일: shush05_thumb.jpg
pause
