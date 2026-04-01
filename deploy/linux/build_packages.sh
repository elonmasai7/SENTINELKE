#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VERSION="${VERSION:-1.0.0}"
OUTDIR="$ROOT/deploy/linux/dist"
APPDIR="$ROOT/deploy/linux/AppDir"

mkdir -p "$OUTDIR" "$APPDIR/usr/bin" "$APPDIR/usr/share/sentinelke"
cp "$ROOT/run_all.py" "$APPDIR/usr/share/sentinelke/run_all.py"
cp "$ROOT/health_check.py" "$APPDIR/usr/share/sentinelke/health_check.py"
cp "$ROOT/.env.prod" "$APPDIR/usr/share/sentinelke/.env.prod"
cat > "$APPDIR/usr/bin/sentinelke" <<'EOF'
#!/usr/bin/env bash
cd /usr/share/sentinelke
exec python3 run_all.py --env-file .env.prod
EOF
chmod +x "$APPDIR/usr/bin/sentinelke"

fpm -s dir -t deb -n sentinelke -v "$VERSION" --prefix / \
  "$APPDIR/usr/bin/sentinelke=/usr/bin/sentinelke" \
  "$APPDIR/usr/share/sentinelke=/usr/share/sentinelke"

mv sentinelke_${VERSION}_amd64.deb "$OUTDIR/sentinelke_${VERSION}_amd64.deb"

fpm -s dir -t rpm -n sentinelke -v "$VERSION" --prefix / \
  "$APPDIR/usr/bin/sentinelke=/usr/bin/sentinelke" \
  "$APPDIR/usr/share/sentinelke=/usr/share/sentinelke"

mv sentinelke-${VERSION}-1.x86_64.rpm "$OUTDIR/sentinelke_${VERSION}.rpm"

appimagetool "$APPDIR" "$OUTDIR/SentinelKE.AppImage"
