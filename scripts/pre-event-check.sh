#!/usr/bin/env bash
# Pre-event check — kesiapan lokal untuk hackathon
echo "check node/python/z3..."
python3 -c "import z3" 2>/dev/null || pip install z3-solver
echo "PRE_EVENT_CHECK_OK"
