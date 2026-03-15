#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_DIR="$ROOT_DIR/skills/continuous-worker"
DIST_DIR="$ROOT_DIR/dist"
TEMPLATE_PATH="$ROOT_DIR/templates/README.release.template.md"
SKILL_FILE="$DIST_DIR/continuous-worker.skill"
README_OUT="$DIST_DIR/continuous-worker.README.md"
SHA_OUT="$DIST_DIR/continuous-worker.skill.sha256"

compute_sha256() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
    return
  fi
  shasum -a 256 "$1" | awk '{print $1}'
}

derive_clawhub_version() {
  local tag="${1:-}"
  if [[ -z "$tag" ]]; then
    printf '0.0.0\n'
    return
  fi
  if [[ "$tag" == continuous-worker-skill-v* ]]; then
    printf '%s\n' "${tag#continuous-worker-skill-v}"
    return
  fi
  if [[ "$tag" == v* ]]; then
    printf '%s\n' "${tag#v}"
    return
  fi
  printf '%s\n' "$tag"
}

resolve_clawhub_version() {
  local tag="${1:-}"
  local explicit_version="${2:-}"
  if [[ -n "$explicit_version" ]]; then
    printf '%s\n' "$explicit_version"
    return
  fi
  derive_clawhub_version "$tag"
}

main() {
  local repo="${GITHUB_REPOSITORY:-}"
  local tag="${GITHUB_REF_NAME:-}"
  local clawhub_version=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --repo)
        repo="${2:-}"
        shift 2
        ;;
      --tag|--version-tag)
        tag="${2:-}"
        shift 2
        ;;
      --version|--clawhub-version)
        clawhub_version="${2:-}"
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

  local sha256
  sha256="$(compute_sha256 "$SKILL_FILE")"
  printf '%s  %s\n' "$sha256" "$(basename "$SKILL_FILE")" > "$SHA_OUT"

  local skill_url
  if [[ -n "$repo" && -n "$tag" ]]; then
    skill_url="https://github.com/$repo/releases/download/$tag/$(basename "$SKILL_FILE")"
  else
    skill_url="https://github.com/<owner>/<repo>/releases/download/<tag>/$(basename "$SKILL_FILE")"
  fi

  clawhub_version="$(resolve_clawhub_version "$tag" "$clawhub_version")"

  local clawhub_cmd
  clawhub_cmd="clawhub publish ./skills/continuous-worker --slug continuous-worker --name \"Continuous Worker\" --version \"$clawhub_version\" --changelog \"Release continuous-worker packaged skill\""

  python3 - <<'PY' \
    "$TEMPLATE_PATH" \
    "$README_OUT" \
    "$(basename "$SKILL_FILE")" \
    "$skill_url" \
    "$sha256" \
    "$clawhub_cmd"
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
  echo
  echo "GitHub import URL:"
  echo "  $skill_url"
  echo
  echo "ClawHub publish command:"
  echo "  $clawhub_cmd"
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  main "$@"
fi
