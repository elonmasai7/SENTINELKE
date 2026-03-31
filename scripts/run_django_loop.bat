@echo off
setlocal

set "ROOT=%~dp0.."
set "STOPFLAG=%ROOT%\.runtime\stop.flag"

:loop
if exist "%STOPFLAG%" goto end

echo [%date% %time%] Starting Django dev server...
python "%ROOT%\backend\manage.py" runserver 127.0.0.1:8010 --settings=sentinelke.settings_local
set "CODE=%ERRORLEVEL%"

if exist "%STOPFLAG%" goto end

echo [%date% %time%] Django exited with code %CODE%. Restarting in 2 seconds...
timeout /t 2 /nobreak >nul
goto loop

:end
echo [%date% %time%] Stop signal received. Django loop exiting.
endlocal
