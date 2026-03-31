@echo off
setlocal

echo Stopping SentinelKE local processes...

taskkill /FI "WINDOWTITLE eq SentinelKE - Django" /T /F >nul 2>nul
taskkill /FI "WINDOWTITLE eq SentinelKE - ML Service" /T /F >nul 2>nul

echo Done.
endlocal
