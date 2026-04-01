@echo off
setlocal

echo Stopping SentinelKE managed processes...
taskkill /IM python.exe /FI "WINDOWTITLE eq *SentinelKE*" /T /F >nul 2>nul
for %%F in (django.pid ml.pid celery.pid ussd.pid llama.pid) do (
  if exist ".runtime\%%F" (
    for /f %%P in (.runtime\%%F) do taskkill /PID %%P /T /F >nul 2>nul
    del /f /q ".runtime\%%F" >nul 2>nul
  )
)

echo Done.
endlocal
