#!/usr/bin/env python
"""
    jdr.benchmark
"""

import json
import base64
import asyncio
import argparse
import numpy as np
import pandas as pd
from time import time
from hashlib import md5
from pathlib import Path
from datasets import load_dataset as hf_load_dataset
from rich import print as rprint

from jdr.agents import ToolCallAgent, JinaDeepsearchAgent, GoogleSearchAgent, SimpleAgent
from jdr.tools import asearch_serp, asearch_serp_multi, ascrape_jina
from jdr.evaluators import MultiEvaluator

DATASET_CONFIGS = {
    "frames" : {
        "path"  : "Intelligent-Internet/frames-benchmark",
        "split" : "benchmark",
    },
    "seal0" : {
        "path"  : "vtllms/sealqa",
        "name"  : "seal_0",
        "split" : "test"
    },
    "simpleqa" : {
        "path"   : "https://openaipublic.blob.core.windows.net/simple-evals/simple_qa_test_set.csv",
    }
}

MODEL_CONFIGS = {
    "gemini/gemini-2.5-flash-preview-05-20": {
        "model"            : "gemini/gemini-2.5-flash-preview-05-20",
        "reasoning_effort" : "medium",
    },
}

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent",           type=str,            default="jdr-toolcall")
    parser.add_argument("--model_name",      type=str,            default="gemini/gemini-2.5-flash-preview-05-20")
    parser.add_argument("--dataset",         type=str,            default="frames")
    parser.add_argument("--sample",          type=int,            default=None)
    parser.add_argument("--seed",            type=int,            default=123)
    parser.add_argument("--mid",             type=str,            default=None, nargs='+')
    parser.add_argument("--no_double_check", action='store_true', default=False)
    args = parser.parse_args()
    
    args.outdir = Path('./results') / args.dataset / args.agent / args.model_name
    args.outdir.mkdir(parents=True, exist_ok=True)
    args.do_double_check = not args.no_double_check

    return args

args = parse_args()
np.random.seed(args.seed)

# --
# IO

if args.dataset == "frames":
    ds = hf_load_dataset(**DATASET_CONFIGS[args.dataset]).to_pandas()
    queries = ds.prompt.to_list()
    targets = ds.answer.to_list()
    special_instructions = "You are only allowed to use Wikipedia as a source of information.  You can prefix your query with `site:wikipedia.org` to search only Wikipedia. Remember to actually visit the webpages using `ascrape_jina`."

elif args.dataset == "seal0":
    ds = hf_load_dataset(**DATASET_CONFIGS[args.dataset]).to_pandas()
    queries = ds.question.tolist()
    targets = ds.answer.tolist()
    special_instructions = "Today's date is June 23, 2025. You strongly prefer using Wikipedia as your source of information.  If you can't completely answer the question using Wikipedia, you're welcome to visit other sites.  Remember to actually visit the webpages using `ascrape_jina`."

elif args.dataset == "simpleqa":
    df      = pd.read_csv(DATASET_CONFIGS[args.dataset]['path'])
    queries = df.problem.tolist()
    targets = df.answer.tolist()
    special_instructions = "Today's date is June 23, 2025. You strongly prefer using Wikipedia as your source of information.  If you can't completely answer the question using Wikipedia, you're welcome to visit other sites.  Remember to actually visit the webpages using `ascrape_jina`."

else:
    raise ValueError(f"Dataset {args.dataset} not supported")

# sample
if args.sample is not None:
    p       = np.random.permutation(len(queries))[:args.sample]
    queries = [queries[i] for i in p]
    targets = [targets[i] for i in p]

# --
# Definte agent

if args.agent == "jdr-toolcall":
    n_concurrent = 8
    agent = ToolCallAgent(
        model_config = MODEL_CONFIGS[args.model_name], 
        tools        = {
            "asearch_serp"       : asearch_serp,
            "asearch_serp_multi" : asearch_serp_multi,
            "ascrape_jina"       : ascrape_jina,
        },
        special_instructions     = special_instructions,
        do_double_check          = args.do_double_check
    ) 
elif args.agent == "jina-deepsearch":
    n_concurrent = 16
    agent = JinaDeepsearchAgent()
elif args.agent == "google-search":
    n_concurrent = 16
    agent = GoogleSearchAgent()
elif args.agent == "simple":
    n_concurrent = 16
    agent = SimpleAgent()
else:
    raise ValueError(f"Agent {args.agent} not supported")

# --
# Run

semaphore = asyncio.Semaphore(n_concurrent)
async def _run_one(query, target, evaluator):
    async with semaphore:
        t   = time()
        mid = md5(query.encode()).hexdigest()
        
        try:
            trace  = await agent.arun(query=query, verbose=False)
            grades = await evaluator.arun(query=query, target=target, response=trace[-1]['content'])
        except Exception as e:
            print(f'ERROR @ _run_one: {e}')
            return None
        
        elapsed = time() - t
        return {
            "mid"     : mid,
            "query"   : query,
            "target"  : target,
            "elapsed" : elapsed,
            "trace"   : trace,
            "grades"  : grades,
        }


async def _run_all():
    evaluator = MultiEvaluator()
    tasks     = [_run_one(query, target, evaluator) for query, target in zip(queries, targets)]
    
    n_errors = 0
    for result in asyncio.as_completed(tasks):
        result = await result
        if result is None:
            n_errors += 1
            rprint(f'[red]n_errors={n_errors}[/red]')
            continue
        
        with open(args.outdir / f"{result['mid']}.json", "w") as f:
            json.dump(result, f)
    
    if n_errors > 0:
        rprint(f'[red]n_errors={n_errors}[/red]')

asyncio.run(_run_all())

