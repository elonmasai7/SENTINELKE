@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"

if not exist "%ROOT%\..\..\.venv" (
  echo Virtual environment not found at %ROOT%\..\..\.venv
  echo Install dependencies, then rerun this script.
)

python -m PyInstaller installer.spec --noconfirm --clean
if errorlevel 1 exit /b 1

if not exist "%ROOT%\dist" mkdir "%ROOT%\dist"
copy /Y "%ROOT%\dist\SentinelKE_Setup.exe" "%ROOT%\..\..\SentinelKE_Setup.exe" >nul

echo Built %ROOT%\..\..\SentinelKE_Setup.exe
endlocal
