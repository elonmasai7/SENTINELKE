@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

echo Running SentinelKE Windows launcher shell...
python desktop\windows\launcher.py --env-file .env.desktop

endlocal
