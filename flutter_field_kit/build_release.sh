#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT/flutter_field_kit"
flutter build apk --release --dart-define-from-file="$ROOT/.env.mobile"
flutter build appbundle --release --dart-define-from-file="$ROOT/.env.mobile"
