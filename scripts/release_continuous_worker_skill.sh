#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_DIR="$ROOT_DIR/skills/continuous-worker"
DIST_DIR="$ROOT_DIR/dist"
TEMPLATE_PATH="$ROOT_DIR/templates/README.release.template.md"
SKILL_FILE="$DIST_DIR/continuous-worker.skill"
README_OUT="$DIST_DIR/continuous-worker.README.md"
SHA_OUT="$DIST_DIR/continuous-worker.skill.sha256"

REPO=""
TAG=""
CLAWHUB_VERSION=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      REPO="${2:-}"
      shift 2
      ;;
    --tag|--version)
      TAG="${2:-}"
      shift 2
      ;;
    --clawhub-version)
      CLAWHUB_VERSION="${2:-}"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

mkdir -p "$DIST_DIR"
python3 "$ROOT_DIR/scripts/package_skill.py" "$SKILL_DIR" "$DIST_DIR" >/dev/null

compute_sha256() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  else
    shasum -a 256 "$1" | awk '{print $1}'
  fi
}

SHA256="$(compute_sha256 "$SKILL_FILE")"
printf '%s  %s\n' "$SHA256" "$(basename "$SKILL_FILE")" > "$SHA_OUT"

if [[ -n "$REPO" && -n "$TAG" ]]; then
  SKILL_URL="https://github.com/$REPO/releases/download/$TAG/$(basename "$SKILL_FILE")"
else
  SKILL_URL="https://github.com/<owner>/<repo>/releases/download/<tag>/$(basename "$SKILL_FILE")"
fi

if [[ -z "$CLAWHUB_VERSION" ]]; then
  CLAWHUB_VERSION="${TAG#continuous-worker-skill-v}"
  [[ -n "$CLAWHUB_VERSION" ]] || CLAWHUB_VERSION="0.0.0"
fi

CLAWHUB_CMD="clawhub publish ./skills/continuous-worker --slug continuous-worker --name \"Continuous Worker\" --version \"$CLAWHUB_VERSION\" --changelog \"Release continuous-worker packaged skill\""

python3 - <<'PY' \
  "$TEMPLATE_PATH" \
  "$README_OUT" \
  "$(basename "$SKILL_FILE")" \
  "$SKILL_URL" \
  "$SHA256" \
  "$CLAWHUB_CMD"
import sys
from pathlib import Path

template_path = Path(sys.argv[1])
output_path = Path(sys.argv[2])
skill_file = sys.argv[3]
skill_url = sys.argv[4]
sha256 = sys.argv[5]
clawhub_cmd = sys.argv[6]

content = template_path.read_text(encoding="utf-8")
content = (
    content.replace("__SKILL_FILE__", skill_file)
    .replace("__SKILL_URL__", skill_url)
    .replace("__SKILL_SHA256__", sha256)
    .replace("__CLAWHUB_PUBLISH_COMMAND__", clawhub_cmd)
)
output_path.write_text(content, encoding="utf-8")
PY

echo "Built:"
echo "  $SKILL_FILE"
echo "  $SHA_OUT"
echo "  $README_OUT"
