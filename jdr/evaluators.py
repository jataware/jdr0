#!/usr/bin/env python
"""
    jdr.evaluators
    
    Autograders for various benchmarks
"""

import os
from functools import partial
from litellm import acompletion
from rich import print as rprint

from jdr.utils import disk_cache

@disk_cache(cache_dir="./.cache/frames_autograder", verbose=False)
async def frames_evaluator(query, target, response):
    """ autograder from the frames paper """
    PROMPT = open(os.path.join(os.path.dirname(__file__), "prompts/frames_evaluator.md")).read()
    PROMPT = PROMPT.format(QUERY=query, TARGET=target, RESPONSE=response)
    PROMPT = PROMPT.strip()
    
    response = await acompletion(
        model    = "gemini/gemini-2.5-pro-preview-06-05", # originally "gemini/gemini-pro-1.5-0514" - no longer available
        messages = [
            {"role" : "system", "content" : "You are a helpful assistant"},
            {"role" : "user", "content" : PROMPT}
        ]
    )
    out = response.choices[0].message.content
    
    decision = out.split("Decision:")[1].strip()
    if decision == 'TRUE':
        correct = True
    else:
        correct = False
    
    return {
        "raw"         : out,
        "explanation" : out.split("Explanation:")[1].split("Decision:")[0].strip(),
        "decision"    : decision,
        "correct"     : correct,
    }

@disk_cache(cache_dir="./.cache/seal_autograder", verbose=False)
async def simpleqa_evaluator(query, target, response, model, no_system_prompt=False, extra_params=None):
    """ autograder from https://github.com/openai/simple-evals """
    if extra_params is None:
        extra_params = {}

    PROMPT = open(os.path.join(os.path.dirname(__file__), "prompts/simpleqa_evaluator.md")).read()
    PROMPT = PROMPT.format(QUERY=query, TARGET=target, RESPONSE=response)
    PROMPT = PROMPT.strip()
    
    messages = [
        {"role" : "system", "content" : "You are a helpful assistant."},
        {"role" : "user", "content" : PROMPT}
    ]
    if no_system_prompt:
        messages = messages[1:]
    
    
    response = await acompletion(
        model       = model,
        messages    = messages,
        **extra_params
    )
    out = response.choices[0].message.content
    out = out.strip().upper()
    
    decision = out
    assert len(decision) == 1
    
    if decision == 'A':
        correct = True
    elif decision in ['B', 'C']:
        correct = False
    else:
        correct = '<format_error>'
    
    return {
        "raw"         : out,
        "explanation" : "<not provided>",
        "decision"    : decision,
        "correct"     : correct,
    }


# --
# Wrapper to run multiple evaluators

EVALUATORS = {
    # from: https://arxiv.org/abs/2409.12941 (reimplemented)
    "frames"   : frames_evaluator,
    
    # from: https://arxiv.org/pdf/2506.01062
    "seal0"    : partial(simpleqa_evaluator, model="gpt-4o-mini"),
    
    # https://github.com/openai/simple-evals/blob/main/simple_evals.py#L255C16-L255C34
    "simpleqa" : partial(simpleqa_evaluator, model="gpt-4.1-2025-04-14", extra_params={"max_tokens" : 2048}),
    
    # https://github.com/sentient-agi/OpenDeepSearch/blob/main/evals/autograde_df.py#L21
    "ods"      : partial(simpleqa_evaluator, model="gemini/gemini-2.0-flash-001", no_system_prompt=True, extra_params={"temperature" : 0.0}),
}

class MultiEvaluator:
    def __init__(self, evaluators=None):
        if evaluators is None:
            self.evaluators = EVALUATORS
        else:
            self.evaluators = {k:EVALUATORS[k] for k in evaluators}
            
        self.n_correct = {k:0 for k in self.evaluators.keys()}
        self.n_total   = 0
        
    async def arun(self, query, target, response, verbose=True):
        grades = {}
        for evaluator_name, evaluator_fn in self.evaluators.items():
            grades[evaluator_name] = await evaluator_fn(
                query    = query,
                target   = target,
                response = response,
            )
            if grades[evaluator_name]['correct']:
                self.n_correct[evaluator_name] += 1
        
        self.n_total += 1
        
        if verbose:
            self.print()
        
        return grades
    
    def print(self):
        _str = ""
        for k, v in self.n_correct.items():
            _str += f'E-{k} - {v:03d}/{self.n_total:03d} - {v/self.n_total:0.4f} | '
        _str = _str.strip(' | ')
        rprint(_str)

