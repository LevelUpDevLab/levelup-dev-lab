#!/usr/bin/env bash
# Sanity test for episode 003: the sample config files exist and are non-empty.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

fail() { echo "FAIL: $1" >&2; exit 1; }

[[ -s "$ROOT/src/.editorconfig" ]] || fail "src/.editorconfig missing or empty"
[[ -s "$ROOT/src/vscode-settings.json" ]] || fail "src/vscode-settings.json missing or empty"
grep -q "root = true" "$ROOT/src/.editorconfig" || fail ".editorconfig missing 'root = true'"

echo "ok - episode 003 sanity test passed"
