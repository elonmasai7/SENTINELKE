#!/usr/bin/env bash
set -euo pipefail
"$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/stop.sh"
sleep 2
"$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run.sh"
