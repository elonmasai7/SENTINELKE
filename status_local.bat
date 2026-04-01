@echo off
setlocal

python health_check.py --env-file .env.dev
endlocal
