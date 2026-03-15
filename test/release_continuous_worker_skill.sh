#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

source ./scripts/release_continuous_worker_skill.sh

assert_eq() {
  local expected="$1"
  local actual="$2"
  if [[ "$expected" != "$actual" ]]; then
    echo "expected: $expected" >&2
    echo "actual:   $actual" >&2
    exit 1
  fi
}

assert_eq "0.1.0" "$(derive_clawhub_version "continuous-worker-skill-v0.1.0")"
assert_eq "1.2.3" "$(derive_clawhub_version "v1.2.3")"
assert_eq "9.9.9" "$(resolve_clawhub_version "continuous-worker-skill-v0.1.0" "9.9.9")"

echo "release_continuous_worker_skill.sh checks passed"
