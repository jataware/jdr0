#!/bin/bash
# Run mechanistic interpretability scorecard generation
#
# Usage:
#   ./run.sh                    # Normal depth (5 benchmarks)
#   ./run.sh quick              # Quick run (3 benchmarks)  
#   ./run.sh deep               # Deep run (7+ benchmarks)
#   ./run.sh deep 6             # Deep run with 6 benchmarks

DEPTH=${1:-normal}
MAX_BENCHMARKS=${2:-5}

echo "=== Running $DEPTH scorecard (max $MAX_BENCHMARKS benchmarks) ==="

pixi run python -m jdr.agents.scorecard_agent \
    --domain "mechanistic interpretability" \
    --depth "$DEPTH" \
    --max-benchmarks "$MAX_BENCHMARKS" \
    --save-data
