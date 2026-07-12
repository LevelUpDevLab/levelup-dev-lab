#!/usr/bin/env bash
# Prints the sample editor config and how to use it.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Sample .editorconfig ($HERE/.editorconfig):"
echo "-----------------------------------------------"
cat "$HERE/.editorconfig"
echo
echo "To use it: copy .editorconfig into the root of any repo and commit it."
echo "Pair it with the editor defaults in vscode-settings.json."
