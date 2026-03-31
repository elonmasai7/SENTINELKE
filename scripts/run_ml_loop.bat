@echo off
setlocal

set "ROOT=%~dp0.."
set "STOPFLAG=%ROOT%\.runtime\stop.flag"

:loop
if exist "%STOPFLAG%" goto end

echo [%date% %time%] Starting ML service...
python -m uvicorn main:app --host 127.0.0.1 --port 9000
set "CODE=%ERRORLEVEL%"

if exist "%STOPFLAG%" goto end

echo [%date% %time%] ML service exited with code %CODE%. Restarting in 2 seconds...
timeout /t 2 /nobreak >nul
goto loop

:end
echo [%date% %time%] Stop signal received. ML loop exiting.
endlocal
