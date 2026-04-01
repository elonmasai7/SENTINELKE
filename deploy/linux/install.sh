#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
INSTALL_DIR="${INSTALL_DIR:-/opt/sentinelke}"
sudo mkdir -p "$INSTALL_DIR"
sudo cp -r "$ROOT"/* "$INSTALL_DIR"/
sudo cp "$ROOT/deploy/linux/sentinelke.service" /etc/systemd/system/sentinelke.service
sudo systemctl daemon-reload
sudo systemctl enable sentinelke.service
sudo systemctl restart sentinelke.service
