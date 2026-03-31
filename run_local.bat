@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"
set "RUNTIME=%ROOT%.runtime"
set "STOPFLAG=%RUNTIME%\stop.flag"

if not exist "%RUNTIME%" mkdir "%RUNTIME%"
if exist "%STOPFLAG%" del /f /q "%STOPFLAG%" >nul 2>nul

echo Starting SentinelKE local stack...
echo.

echo Opening Django terminal...
start "SentinelKE - Django" cmd /k "cd /d ""%ROOT%"" && call scripts\run_django_loop.bat"

echo Opening ML service terminal...
start "SentinelKE - ML Service" cmd /k "cd /d ""%ROOT%\ml_services"" && call ..\scripts\run_ml_loop.bat"

echo.
echo Django:     http://127.0.0.1:8010
echo ML service: http://127.0.0.1:9000/health
echo.
echo Services will auto-restart if they crash.
echo Use stop_local.bat to stop both processes.

endlocal
