@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%\flutter_field_kit"

echo Running SentinelKE desktop app (Windows target)...
flutter run -d windows

endlocal
