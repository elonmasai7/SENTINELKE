@echo off
setlocal

set "DJANGO_URL=http://127.0.0.1:8010/"
set "ML_URL=http://127.0.0.1:9000/health"

set "DJANGO_STATUS=DOWN"
set "ML_STATUS=DOWN"
set "DJANGO_CODE=-"
set "ML_CODE=-"

for /f %%A in ('powershell -NoProfile -Command "try { (Invoke-WebRequest -UseBasicParsing '%DJANGO_URL%' -TimeoutSec 3).StatusCode } catch { 0 }"') do set DJANGO_CODE=%%A
for /f %%A in ('powershell -NoProfile -Command "try { (Invoke-WebRequest -UseBasicParsing '%ML_URL%' -TimeoutSec 3).StatusCode } catch { 0 }"') do set ML_CODE=%%A

if not "%DJANGO_CODE%"=="0" set "DJANGO_STATUS=UP"
if not "%ML_CODE%"=="0" set "ML_STATUS=UP"

echo Local Service Status
echo --------------------
echo Django (%DJANGO_URL%): %DJANGO_STATUS% [HTTP %DJANGO_CODE%]
echo ML Service (%ML_URL%): %ML_STATUS% [HTTP %ML_CODE%]

if "%DJANGO_STATUS%"=="UP" if "%ML_STATUS%"=="UP" (
  exit /b 0
)

exit /b 1
endlocal
