#!/bin/sh
# Full sprite pipeline: harness -> capture -> alpha/crop -> PIL shapes.
set -e
cd "$(dirname "$0")/.."
python3 render/build_harness.py
python3 render/specs.py
(cd render && node capture.mjs)
python3 render/postprocess.py > /dev/null
python3 gen/art_extra.py
