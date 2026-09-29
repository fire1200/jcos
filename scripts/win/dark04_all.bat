@echo off
chcp 65001 >nul
rem ============================================================
rem 10/6 #4 어두운 화면 3시간 - 한 번에 끝내기
rem 안내서: todam/dark04_finish.md
rem
rem 준비 (둘 중 하나):
rem   1) 기존 "3시간 무가사 피아노" 원본 파일을 이 배치 파일 아이콘 위로 끌어다 놓기 (복사 불필요)
rem   2) 같은 폴더에 muga_3h_source 라는 이름으로 넣고 더블클릭 (확장자는 그대로)
rem       이미지·글자 파일은 필요 없습니다. 전부 자동으로 만듭니다.
rem 필요: ffmpeg full 빌드 (drawtext 포함)
rem 결과: Dark04_Upload.mp4, dark04_thumb.jpg
rem 이미 만든 결과 파일은 건너뜁니다. 다시 만들려면 그 파일을 지우세요.
rem ============================================================
setlocal
cd /d "%~dp0"
set FONT=C\:/Windows/Fonts/malgunbd.ttf
set SRC=
for %%F in (muga_3h_source.*) do set SRC=%%F
if not "%~1"=="" set "SRC=%~1"
set FINAL=Dark04_Final.wav
set UPLOAD=Dark04_Upload.mp4

where ffmpeg >nul 2>nul || (echo ffmpeg를 찾을 수 없습니다. & pause & exit /b 1)
if "%SRC%"=="" (echo 원본이 없습니다. 원본 파일을 배치 파일 위로 끌어다 놓거나 muga_3h_source 로 이름을 바꿔 넣으세요. & pause & exit /b 1)
if not exist "%SRC%" (echo 원본 파일을 찾을 수 없습니다: %SRC% & pause & exit /b 1)
echo 원본: %SRC%

echo.
echo [1/5] 최종 음원 - 핑크노이즈와 음량 정리, 약 10~20분
if exist %FINAL% (echo       이미 있음, 건너뜀) else (
ffmpeg -v error -stats -y -i "%SRC%" -f lavfi -i "anoisesrc=color=pink:sample_rate=48000:amplitude=1:seed=20261006" -filter_complex "[0:a]aformat=channel_layouts=stereo,acompressor=threshold=-30dB:ratio=2.5:attack=200:release=3000:makeup=1,loudnorm=I=-16:LRA=4:TP=-1.5,aresample=48000[m];[1:a]lowpass=f=10000,lowpass=f=10000,volume=-28dB,aformat=channel_layouts=stereo[bed];[m][bed]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,loudnorm=I=-16:LRA=4:TP=-1.5,aresample=48000[out]" -map "[out]" -map_metadata -1 -c:a pcm_s24le -ar 48000 -t 10800 %FINAL%
)
if not exist %FINAL% (echo 최종 음원 만들기 실패 & pause & exit /b 1)

echo.
echo [2/5] 별 배경과 썸네일
if not exist dark04_stars.png ffmpeg -v error -y -f lavfi -i "nullsrc=s=1920x1080:d=1,format=gray" -vf "geq=lum='if(gt(random(1),0.99955),90+random(2)*120,0)',gblur=sigma=1.2" -frames:v 1 dark04_stars.png
echo 어두운 화면> dark04_thumb.txt
ffmpeg -v error -y -f lavfi -i "color=c=0x070A14:s=1280x720:d=1" -f lavfi -i "color=c=0xF4F1FF:s=1280x720:d=1" -i dark04_stars.png -filter_complex "[2:v]format=gray,dilation,dilation,scale=1280:720,lut=y='min(255,val*2.2)'[m];[1:v]format=rgba[w];[w][m]alphamerge[st];[0:v][st]overlay=format=auto,format=gbrp,geq=r='if(lt(hypot(X-1040,Y-200),88)*gte(hypot(X-1076,Y-176),82),245,r(X,Y))':g='if(lt(hypot(X-1040,Y-200),88)*gte(hypot(X-1076,Y-176),82),200,g(X,Y))':b='if(lt(hypot(X-1040,Y-200),88)*gte(hypot(X-1076,Y-176),82),107,b(X,Y))',format=yuv444p,drawtext=fontfile='%FONT%':textfile=dark04_thumb.txt:fontsize=132:fontcolor=0xFFF6E5:shadowcolor=black@0.7:shadowx=4:shadowy=4:x=80:y=h-th-90" -frames:v 1 -q:v 2 dark04_thumb.jpg

echo.
echo [3/5] 30분 반복 배경 영상 - 약 20~30분
if exist dark04_loop30.mp4 (echo       이미 있음, 건너뜀) else (
ffmpeg -v error -stats -y -loop 1 -framerate 30 -t 1800 -i dark04_stars.png -f lavfi -i "color=c=0x05070D:s=1920x1080:r=30:d=1800" -f lavfi -i "color=c=0xDDE3FF:s=1920x1080:r=30:d=1800" -filter_complex "[0:v]format=gray,split[a][b];[a][b]hstack,crop=1920:1080:x='mod(t*1920/1800,1920)':y=0[m];[2:v]format=rgba[w];[w][m]alphamerge[st];[1:v][st]overlay=format=auto,eq=brightness='0.006*sin(2*PI*t/60)':eval=frame,format=yuv420p[v]" -map "[v]" -c:v libx264 -preset slow -crf 30 -tune stillimage -g 300 -r 30 dark04_loop30.mp4
)
if not exist dark04_loop30.mp4 (echo 배경 영상 만들기 실패 & pause & exit /b 1)

echo.
echo [4/5] 3시간 업로드 영상 - 수 분
ffmpeg -v error -stats -y -stream_loop -1 -i dark04_loop30.mp4 -i %FINAL% -map 0:v -map 1:a -c:v copy -c:a aac -b:a 384k -t 10800 -movflags +faststart %UPLOAD%
if errorlevel 1 (echo 업로드 영상 만들기 실패 & pause & exit /b 1)

echo.
echo [5/5] 결과 측정 - 합격: I -17~-14 LUFS, LRA 4 이하, Peak -1.5 이하, 길이 10800초
ffmpeg -hide_banner -nostats -i %FINAL% -af ebur128=peak=true:framelog=quiet -f null - 2>&1 | findstr /C:"I:" /C:"LRA:" /C:"Peak:"
ffprobe -v error -show_entries format=duration -of default=nw=1 %UPLOAD%

echo.
echo 완료: %UPLOAD% / 썸네일: dark04_thumb.jpg
pause
