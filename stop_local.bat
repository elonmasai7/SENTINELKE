@echo off
setlocal

echo Stopping SentinelKE local processes...

set "ROOT=%~dp0"
set "RUNTIME=%ROOT%.runtime"
set "STOPFLAG=%RUNTIME%\stop.flag"

if not exist "%RUNTIME%" mkdir "%RUNTIME%"
echo stop>"%STOPFLAG%"

taskkill /FI "WINDOWTITLE eq SentinelKE - Django" /T /F >nul 2>nul
taskkill /FI "WINDOWTITLE eq SentinelKE - ML Service" /T /F >nul 2>nul

echo Done.
endlocal
