@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%\flutter_field_kit"

echo Running SentinelKE mobile app (Android target)...
flutter run -d android --dart-define-from-file="%ROOT%\.env.mobile"

endlocal
