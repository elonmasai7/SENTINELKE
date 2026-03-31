@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

echo Starting SentinelKE local stack...
echo.

echo Opening Django terminal...
start "SentinelKE - Django" cmd /k "cd /d ""%ROOT%"" && python backend\manage.py runserver 127.0.0.1:8010 --settings=sentinelke.settings_local"

echo Opening ML service terminal...
start "SentinelKE - ML Service" cmd /k "cd /d ""%ROOT%\ml_services"" && python -m uvicorn main:app --host 127.0.0.1 --port 9000"

echo.
echo Django:     http://127.0.0.1:8010
echo ML service: http://127.0.0.1:9000/health
echo.
echo Use stop_local.bat to stop both processes.

endlocal
