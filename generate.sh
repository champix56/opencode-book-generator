#!/usr/bin/env sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if ! command -v python3 >/dev/null 2>&1; then echo 'Python 3 est requis.' >&2; exit 127; fi
exec python3 "$ROOT/generators/bookgen.py" "$@"
