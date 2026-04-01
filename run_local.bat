@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"
echo Starting SentinelKE orchestrated local stack...
python run_all.py --env-file .env.dev

endlocal
