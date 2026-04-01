@echo off
setlocal
set "ROOT=%~dp0..\"
cd /d "%ROOT%\flutter_field_kit"
flutter build apk --release --dart-define-from-file="%ROOT%\.env.mobile"
flutter build appbundle --release --dart-define-from-file="%ROOT%\.env.mobile"
endlocal
