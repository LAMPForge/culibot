#! /bin/bash

set -euo pipefail
set -x

cd /workspace/server
poetry install
echo "✅ Server ready"
