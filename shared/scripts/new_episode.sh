#!/usr/bin/env bash
#
# new_episode.sh — scaffold a new episode folder from the shared template.
#
# Usage:
#   shared/scripts/new_episode.sh <number> <slug> [title]
#
# Examples:
#   shared/scripts/new_episode.sh 7 automation-file-watcher
#   shared/scripts/new_episode.sh 007 automation-file-watcher "Automation: File Watcher"
#
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <number> <slug> [title]" >&2
  echo "  e.g. $0 7 automation-file-watcher \"Automation: File Watcher\"" >&2
  exit 1
fi

# Resolve repo root relative to this script (shared/scripts/ -> repo root).
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

NUMBER_RAW="$1"
SLUG="$2"
TITLE="${3:-${SLUG//-/ }}"

# Zero-pad the number to three digits (7 -> 007).
if ! [[ "${NUMBER_RAW}" =~ ^[0-9]+$ ]]; then
  echo "Error: number must be numeric, got '${NUMBER_RAW}'" >&2
  exit 1
fi
NUMBER="$(printf '%03d' "$((10#${NUMBER_RAW}))")"

# Validate slug (lowercase letters, digits, hyphens).
if ! [[ "${SLUG}" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "Error: slug must be lowercase-with-hyphens, got '${SLUG}'" >&2
  exit 1
fi

EPISODE_DIR="${REPO_ROOT}/episodes/${NUMBER}-${SLUG}"
TEMPLATE="${REPO_ROOT}/shared/templates/episode-readme.md"

if [[ -e "${EPISODE_DIR}" ]]; then
  echo "Error: ${EPISODE_DIR} already exists" >&2
  exit 1
fi
if [[ ! -f "${TEMPLATE}" ]]; then
  echo "Error: template not found at ${TEMPLATE}" >&2
  exit 1
fi

echo "Creating episode ${NUMBER}-${SLUG} ..."
mkdir -p "${EPISODE_DIR}/src" "${EPISODE_DIR}/tests"

# Render the README from the template with simple placeholder substitution.
sed \
  -e "s/{{NUMBER}}/${NUMBER}/g" \
  -e "s/{{TITLE}}/${TITLE}/g" \
  -e "s/{{PILLAR}}/TODO/g" \
  -e "s/{{LANGUAGES}}/TODO/g" \
  "${TEMPLATE}" > "${EPISODE_DIR}/README.md"

# Minimal Makefile so `make setup/run/test` exist from day one.
cat > "${EPISODE_DIR}/Makefile" <<'MAKE'
.PHONY: setup run test

setup:
	@echo "TODO: install this episode's dependencies"

run:
	@echo "TODO: run this episode's example"

test:
	@echo "TODO: add a sanity test for this episode"
MAKE

# Placeholder src/tests so the folders are not empty.
echo "// TODO: episode source goes here" > "${EPISODE_DIR}/src/.gitkeep"
echo "// TODO: episode tests go here" > "${EPISODE_DIR}/tests/.gitkeep"

echo "Done: episodes/${NUMBER}-${SLUG}"
echo "Next: edit its README.md, add src/ + tests/, and wire up the Makefile."
