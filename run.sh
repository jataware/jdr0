#!/bin/bash
# Run mechanistic interpretability scorecard generation

# Simple out-of-box run
echo "=== Running simple scorecard ==="
pixi run python -c "
import asyncio
from jdr.agents import ToolCallAgent
from jdr.tools import aarxiv_search, aarxiv_fetch

agent = ToolCallAgent(
    model_config = {'model': 'gemini/gemini-2.5-flash', 'reasoning_effort': 'medium'},
    tools = {
        'aarxiv_search': aarxiv_search,
        'aarxiv_fetch': aarxiv_fetch,
    },
    special_instructions = 'Use aarxiv_search and aarxiv_fetch to find papers. Be thorough.',
    do_double_check = False,
)

query = '''Create a papers-with-code style SOTA scorecard for mechanistic interpretability research.
Include: benchmarks/datasets, key methods, quantitative results, and which methods perform best.
Format as structured tables.'''

result = asyncio.run(agent.arun(query, max_iters=15))
"

# Staged multi-step run
echo "=== Running staged scorecard ==="
pixi run python -m jdr.agents.scorecard_agent \
    --domain "mechanistic interpretability" \
    --max-benchmarks 3 \
    --save-data
