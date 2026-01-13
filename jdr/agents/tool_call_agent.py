#!/usr/bin/env python
"""
    jdr.agents.tool_call_agent
    
    (Baseline) Tool-calling agent
"""

import os
os.environ["DEFER_PYDANTIC_BUILD"] = "0"

import asyncio
from copy import deepcopy
from litellm import acompletion
from rich.console import Console
from rich import print as rprint

from jdr.tools import ToolBox
from jdr.utils import disk_cache
from jdr.pretty import print_msg, print_tool_result

__all__ = ["ToolCallAgent"]

DOUBLE_CHECK_PROMPT = """
Great!  Thanks.  Can you go back and double-check your initial answer?

Make sure you didn't hallucinate any facts, and that you've actually visited and read the webpages you've cited!  

Once you've finalized your answer, please output your FINAL ANSWER using the same <output>...</output> schema as before.
The user is not going to see your initial answer.  Your final answer should be standalone.  

If you find that the initial answer could not find the information to answer the question, you likely need to use your tools (search, scrape, follow links, etc) to keep looking.
""".strip()

SYSTEM_PROMPT = "jdr/prompts/tool_call_agent_v2.md"

# --
# Helpers

def _drop_bad_fields(message):
    BAD = ['reasoning_content', 'provider_specific_fields']
    return {k:v for k,v in message.items() if k not in BAD}

@disk_cache(cache_dir="./.cache/completion", verbose=False)
async def _cached_acompletion(*args, **kwargs):
    return await acompletion(*args, **kwargs)

# --
# Agent

class ToolCallAgent:
    def __init__(self, model_config, tools, special_instructions=None, do_double_check=False):
        self.model_config = model_config
        
        force_lowercase = model_config['model'] in ['gpt-4o', 'o3-mini']
        self.toolbox    = ToolBox(tools, force_lowercase=force_lowercase)
        
        self.system_prompt_template = open(SYSTEM_PROMPT).read()
        self.special_instructions   = special_instructions
        self.double_check_prompt    = DOUBLE_CHECK_PROMPT
        
        self._acompletion           = _cached_acompletion
        self.do_double_check        = do_double_check
    
    def _get_system_prompt(self):
        SYSTEM_PROMPT = self.system_prompt_template.format( # TODO: add TOOLS
            TOOLS="\n\n".join([f"- {v['function']['name']}: {v['function']['description']}" for v in self.toolbox.sigs])
        )
        if self.special_instructions:
            SYSTEM_PROMPT += f"\n\nIMPORTANT:\n{self.special_instructions}"
        return SYSTEM_PROMPT

    
    async def arun(self, query, max_iters=100, verbose=True):
        console = Console()
        
        messages = [
            {"role" : "system", "content" : self._get_system_prompt()},
            {"role" : "user",   "content" : query},
        ]
        
        if verbose:
            for msg in messages:
                print_msg(msg, console=console)

        DOUBLE_CHECK_COMPLETED = False
        for _ in range(max_iters):
            out = await self._acompletion(
                **self.model_config,
                messages = [_drop_bad_fields(m) for m in messages],
                tools    = deepcopy(self.toolbox.sigs), # [LITELLM BUG] they change the list?  `OBJECT` -> `object`
            )
            message = out.choices[0].message
            
            if verbose:
                print_msg(message, console=console)
            
            # --
            # Tool call
            
            if message.tool_calls:
                if 'provider_specific_fields' in message:
                    del message.provider_specific_fields
                
                messages.append({
                    "role"              : message.role,
                    "content"           : message.content,
                    "reasoning_content" : message.reasoning_content if hasattr(message, 'reasoning_content') else None,
                    "tool_calls"        : [tool_call.model_dump() for tool_call in message.tool_calls],
                })
                
                tool_result_msgs = await asyncio.gather(*[
                    self.toolbox.arun(tool_call) for tool_call in message.tool_calls
                ])
                
                if verbose:
                    for tool_result_msg in tool_result_msgs:
                        print_tool_result(tool_result_msg, console=console)
                
                messages += tool_result_msgs
            else:
                messages.append({
                    "role"              : message.role,
                    "content"           : message.content,
                    "reasoning_content" : message.reasoning_content if hasattr(message, 'reasoning_content') else None,
                })
                
                if not self.do_double_check:
                    break
                elif DOUBLE_CHECK_COMPLETED:
                    break
                else:
                    DOUBLE_CHECK_COMPLETED = True
                    messages.append({
                        "role"    : "user",
                        "content" : self.double_check_prompt,
                    })
        
        if messages[-1]['content'] is None:
            rprint("[yellow]WARNING | ToolCallAgent: messages[-1]['content'] is None - rolling back[/yellow]")
            messages = messages[:-2]
        
        return messages


# --
# CLI for testing

if __name__ == "__main__":
    import argparse
    
    from jdr.tools import asearch_serp, asearch_serp_multi, ascrape_jina, aarxiv_search, aarxiv_fetch
    from jdr.evaluators import EVALUATORS
    
    MODEL_CONFIGS = {
        "gemini/gemini-2.5-flash": {
            "model"            : "gemini/gemini-2.5-flash",
            "reasoning_effort" : "medium",
        },
        "gemini/gemini-2.5-pro": {
            "model"            : "gemini/gemini-2.5-pro",
            "reasoning_effort" : "medium",
        },
    }
        
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, default="gemini/gemini-2.5-pro")
    parser.add_argument("--query",      type=str, required=True)
    parser.add_argument("--target",     type=str)
    parser.add_argument("--evaluator",  type=str, choices=EVALUATORS.keys())
    args = parser.parse_args()
    
    agent = ToolCallAgent(
        model_config = MODEL_CONFIGS[args.model_name], 
        tools        = {
            "asearch_serp"       : asearch_serp,
            "asearch_serp_multi" : asearch_serp_multi,
            "ascrape_jina"       : ascrape_jina,
            "aarxiv_search"      : aarxiv_search,
            "aarxiv_fetch"       : aarxiv_fetch,
        },
        special_instructions = "Today's date is June 23, 2025. You strongly prefer using Wikipedia as your source of information.  If you can't completely answer the question using Wikipedia, you're welcome to visit other sites.  Remember to actually visit the webpages using `ascrape_jina`.",
        do_double_check      = True,
    )
    
    result = asyncio.run(agent.arun(args.query))
    
    if args.evaluator:
        assert args.target is not None, "Target is required for evaluation"
        evaluator = EVALUATORS[args.evaluator]
        grade     = asyncio.run(evaluator(args.query, args.target, result))
        rprint(grade)