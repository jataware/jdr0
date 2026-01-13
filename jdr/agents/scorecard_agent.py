#!/usr/bin/env python
"""
    jdr.agents.scorecard_agent
    
    Multi-stage agent for generating SOTA scorecards
    
    Stage 1: Discover benchmarks/datasets in a domain
    Stage 2: For each benchmark, find methods and results
    Stage 3: Synthesize into structured scorecard
"""

import asyncio
import json
from rich.console import Console
from rich import print as rprint

from jdr.agents import ToolCallAgent
from jdr.tools import aarxiv_search, aarxiv_fetch

console = Console()

# Stage-specific prompts
STAGE1_DISCOVER_PROMPT = """Your task is to discover ALL major benchmarks and datasets used in {domain} research.

Search arXiv thoroughly with multiple queries to find:
1. Benchmark papers that introduce evaluation frameworks
2. Survey/review papers that list existing benchmarks
3. Papers that compare methods on standard datasets

Output a JSON list of benchmarks found:
```json
{{
  "benchmarks": [
    {{
      "name": "Benchmark Name",
      "arxiv_id": "XXXX.XXXXX",
      "description": "Brief description",
      "tasks": ["task1", "task2"],
      "metrics": ["metric1", "metric2"]
    }}
  ]
}}
```

Be exhaustive - search with different query variations to maximize coverage."""

STAGE2_METHODS_PROMPT = """Your task is to find all methods evaluated on the benchmark: {benchmark_name}

Search arXiv for papers that:
1. Introduce new methods tested on this benchmark
2. Report results/scores on this benchmark
3. Compare multiple methods on this benchmark

For the benchmark "{benchmark_name}" ({benchmark_description}), extract:
- Method names
- Quantitative scores on key metrics
- Which paper reported each result

Output as JSON:
```json
{{
  "benchmark": "{benchmark_name}",
  "results": [
    {{
      "method": "Method Name",
      "arxiv_id": "XXXX.XXXXX", 
      "scores": {{
        "metric1": 0.XX,
        "metric2": 0.XX
      }},
      "notes": "any relevant notes"
    }}
  ]
}}
```"""

STAGE3_SYNTHESIZE_PROMPT = """You have collected benchmark and results data for {domain}.

Here is the collected data:
{collected_data}

Synthesize this into a comprehensive SOTA scorecard with:

1. **Benchmark Overview Table**: All benchmarks with their tasks and metrics
2. **Leaderboard Tables**: For each benchmark, a table of methods ranked by performance  
3. **Method Summary**: Key techniques and which benchmarks they excel on
4. **Gaps & Opportunities**: Areas lacking standardized evaluation

Format with clear markdown tables. Highlight SOTA results."""


async def run_stage(agent, query, stage_name):
    """Run a single stage and return the final message content."""
    console.rule(f"[bold blue]{stage_name}[/bold blue]")
    messages = await agent.arun(query, max_iters=10, verbose=True)
    
    # Extract final answer
    final_content = messages[-1].get('content', '')
    return final_content


async def extract_json(content):
    """Try to extract JSON from agent response."""
    import re
    # Look for JSON blocks
    json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    return None


def extract_final_answer(content: str) -> str:
    """Extract clean answer from <output><answer>...</answer></output> tags."""
    import re
    
    # Try to extract from <answer> tags first
    answer_match = re.search(r'<answer>\s*(.*?)\s*</answer>', content, re.DOTALL)
    if answer_match:
        clean = answer_match.group(1).strip()
    else:
        # Try to extract from <output> tags
        output_match = re.search(r'<output>\s*(.*?)\s*</output>', content, re.DOTALL)
        if output_match:
            clean = output_match.group(1).strip()
        else:
            # Fallback: use content as-is
            clean = content
    
    # Clean up any remaining XML-style tags
    clean = re.sub(r'</?output>', '', clean)
    clean = re.sub(r'</?answer>', '', clean)
    clean = re.sub(r'<citations>.*?</citations>', '', clean, flags=re.DOTALL)
    clean = re.sub(r'<url>.*?</url>', '', clean, flags=re.DOTALL)
    
    # Remove reasoning content if present
    clean = re.sub(r'Reasoning:.*?(?=Content:|$)', '', clean, flags=re.DOTALL)
    
    return clean.strip()


async def run_scorecard_pipeline(domain: str, max_benchmarks: int = 5):
    """
    Run the full multi-stage scorecard generation pipeline.
    
    Args:
        domain: Research domain (e.g., "mechanistic interpretability")
        max_benchmarks: Max benchmarks to deep-dive on in stage 2
    """
    
    # Create agent with arxiv tools
    agent = ToolCallAgent(
        model_config={'model': 'gemini/gemini-2.5-flash', 'reasoning_effort': 'medium'},
        tools={
            'aarxiv_search': aarxiv_search,
            'aarxiv_fetch': aarxiv_fetch,
        },
        special_instructions='Use aarxiv_search and aarxiv_fetch to find papers. Be thorough.',
        do_double_check=False,
    )
    
    collected_data = {"domain": domain, "benchmarks": [], "results": {}}
    
    # =========== STAGE 1: Discover Benchmarks ===========
    stage1_query = STAGE1_DISCOVER_PROMPT.format(domain=domain)
    stage1_result = await run_stage(agent, stage1_query, "Stage 1: Discover Benchmarks")
    
    # Try to parse benchmarks
    stage1_json = await extract_json(stage1_result)
    if stage1_json and 'benchmarks' in stage1_json:
        collected_data['benchmarks'] = stage1_json['benchmarks']
        rprint(f"[green]Found {len(collected_data['benchmarks'])} benchmarks[/green]")
    else:
        # Fallback: store raw text
        collected_data['stage1_raw'] = stage1_result
        rprint("[yellow]Could not parse benchmarks JSON, stored raw text[/yellow]")
    
    # =========== STAGE 2: Get Methods & Results for Each Benchmark ===========
    benchmarks_to_query = collected_data.get('benchmarks', [])[:max_benchmarks]
    
    for i, benchmark in enumerate(benchmarks_to_query):
        bench_name = benchmark.get('name', f'Benchmark {i+1}')
        bench_desc = benchmark.get('description', '')
        
        stage2_query = STAGE2_METHODS_PROMPT.format(
            benchmark_name=bench_name,
            benchmark_description=bench_desc
        )
        
        stage2_result = await run_stage(
            agent, 
            stage2_query, 
            f"Stage 2: Methods for {bench_name}"
        )
        
        stage2_json = await extract_json(stage2_result)
        if stage2_json:
            collected_data['results'][bench_name] = stage2_json
        else:
            collected_data['results'][bench_name] = {'raw': stage2_result}
    
    # =========== STAGE 3: Synthesize Final Scorecard ===========
    # Create a synthesis agent (no tools needed, just reasoning)
    synthesis_agent = ToolCallAgent(
        model_config={'model': 'gemini/gemini-2.5-flash', 'reasoning_effort': 'medium'},
        tools={},  # No tools for synthesis
        special_instructions='Synthesize the provided data into a well-structured scorecard.',
        do_double_check=False,
    )
    
    stage3_query = STAGE3_SYNTHESIZE_PROMPT.format(
        domain=domain,
        collected_data=json.dumps(collected_data, indent=2)
    )
    
    final_result = await run_stage(synthesis_agent, stage3_query, "Stage 3: Synthesize Scorecard")
    
    # Extract clean document from the response
    clean_scorecard = extract_final_answer(final_result)
    
    return {
        'domain': domain,
        'collected_data': collected_data,
        'final_scorecard_raw': final_result,
        'final_scorecard': clean_scorecard,
    }


# CLI
if __name__ == "__main__":
    import argparse
    import os
    from datetime import datetime
    
    parser = argparse.ArgumentParser(description="Generate SOTA scorecard for a research domain")
    parser.add_argument("--domain", type=str, default="mechanistic interpretability",
                        help="Research domain to generate scorecard for")
    parser.add_argument("--max-benchmarks", type=int, default=3,
                        help="Maximum benchmarks to deep-dive on")
    parser.add_argument("--output-dir", type=str, default="reports",
                        help="Output directory for results")
    parser.add_argument("--save-data", action="store_true",
                        help="Also save raw collected data as JSON")
    args = parser.parse_args()
    
    result = asyncio.run(run_scorecard_pipeline(args.domain, args.max_benchmarks))
    
    # Sanitize domain for filename
    domain_slug = args.domain.replace(' ', '_').lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Save clean markdown document
    md_path = os.path.join(args.output_dir, f"{domain_slug}_scorecard.md")
    with open(md_path, 'w') as f:
        f.write(f"# SOTA Scorecard: {args.domain.title()}\n\n")
        f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write("---\n\n")
        f.write(result['final_scorecard'])
    rprint(f"[green]✓ Scorecard saved to {md_path}[/green]")
    
    # Optionally save raw data
    if args.save_data:
        json_path = os.path.join(args.output_dir, f"{domain_slug}_data.json")
        with open(json_path, 'w') as f:
            json.dump(result, f, indent=2)
        rprint(f"[green]✓ Raw data saved to {json_path}[/green]")
    
    # Print final scorecard
    console.rule("[bold green]FINAL SCORECARD[/bold green]")
    rprint(result['final_scorecard'])
