#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if command -v python >/dev/null 2>&1; then
	PYTHON_BIN="python"
elif command -v python3 >/dev/null 2>&1; then
	PYTHON_BIN="python3"
else
	echo "Error: neither 'python' nor 'python3' was found in PATH." >&2
	exit 1
fi

cd "$ROOT_DIR/api"
"$PYTHON_BIN" -m tasks.export_openapi

cd "$ROOT_DIR"
openapi-typescript api/openapi.json -o packages/shared/src/api/schema.d.ts
