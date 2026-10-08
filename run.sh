#!/usr/bin/env bash
# Chay pi nhu mot agent rieng chi ve CAD / dung sai - nham be mat.
export PI_CODING_AGENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pi "$@"
