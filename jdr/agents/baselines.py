#!/usr/bin/env python3
"""
    jdr.agents.baselines
"""

import os
import httpx
from litellm import acompletion

from jdr.pretty import print_msg
from jdr.utils import disk_cache_fn

async def jina_deepsearch(query, model='jina-deepsearch-v2'):
    JINA_API_KEY = os.getenv('JINA_API_KEY')
    if not JINA_API_KEY:
        raise ValueError('JINA_API_KEY is not set')

    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post(
            'https://deepsearch.jina.ai/v1/chat/completions', 
            headers = {
                'Content-Type'  : 'application/json',
                'Authorization' : f'Bearer {JINA_API_KEY}'
            }, 
            json    = {
                "model"            : model,
                "messages"         : [{"role" : "user", "content" : query}],
                "stream"           : False,
                "reasoning_effort" : "medium",
                "max_attempts"     : 1,
                "no_direct_answer" : False
            }
        )
    return response.json()

class JinaDeepsearchAgent:
    def __init__(self, model='jina-deepsearch-v2'):
        self.model = model
        self._jina_deepsearch = disk_cache_fn(jina_deepsearch, cache_dir="./.cache/jina_deepsearch", verbose=False)
    
    async def arun(self, query, **kwargs):
        out = await self._jina_deepsearch(query, self.model)
        return [
            {
                "role"    : "user",
                "content" : query
            },
            {
                "role"    : "assistant",
                "content" : out['choices'][0]['message']['content']
            }
        ]


# --

GOOGLE_SEARCH_SYSTEM_PROMPT = """
You are a helpful assistant that can use Google search to answer queries.

Many queries are complex and may require multiple searches.

Some information on the internet is unreliable - you should prioritize trusted sources and find corroborating evidence when appropriate.

First, think about the query carefully.  Write a section titled "Ambiguities" enumerating any ambiguities in the query language.

Second, write a plan in pseudo-code for how you are going to answer the query.  Then start your research.

Your final answer should be in the following format:

```
<output>
    <answer>
    ...
    </answer>
    <citations>
        <url>
        ...
        </url>
    </citations>
</output>
```

Today's date is June 23, 2025. You strongly prefer using Wikipedia as your source of information.  You can prefix your query with `site:wikipedia.org` to search only Wikipedia. If the information is not available on Wikipedia, you can then use other websites.
"""

class GoogleSearchAgent:
    def __init__(self):
        self._acompletion = disk_cache_fn(acompletion, cache_dir="./.cache/completion", verbose=False)
    
    async def arun(self, query, **kwargs):
        
        messages = [
            {"role" : "system", "content" : GOOGLE_SEARCH_SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
        
        response = await self._acompletion(
            model = "gemini/gemini-2.5-flash-preview-05-20",
            messages = messages,
            tools = [{"googleSearch": {}}],
            reasoning_effort = "medium"
        )
        
        messages.append({
            "role"              : "assistant",
            "content"           : response.choices[0].message.content,
            "reasoning_content" : response.choices[0].message.reasoning_content
        })
        
        return messages

# --

SIMPLE_SYSTEM_PROMPT = """
You are a helpful assistant that answers queries.

First, think about the query carefully.

Then answer the query.

Your final answer should be in the following format:

```
<output>
    <answer>
    ...
    </answer>
</output>
```

Today's date is June 23, 2025.
"""

class SimpleAgent:
    def __init__(self):
        self._acompletion = disk_cache_fn(acompletion, cache_dir="./.cache/completion", verbose=False)
    
    async def arun(self, query, **kwargs):
        
        messages = [
            {"role" : "system", "content" : SIMPLE_SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
        
        response = await self._acompletion(
            model = "gemini/gemini-2.5-flash-preview-05-20",
            messages = messages,
            reasoning_effort = "medium"
        )
        
        messages.append({
            "role"              : "assistant",
            "content"           : response.choices[0].message.content,
            "reasoning_content" : response.choices[0].message.reasoning_content
        })
        
        return messages



__all__ = ["JinaDeepsearchAgent", "GoogleSearchAgent", "SimpleAgent"]

if __name__ == '__main__':
    import asyncio
    
    query = "Who broke the short course world record in women's 400m freestyle at the youngest age from 2010 to now?"
    agent = SimpleAgent()
    trace = asyncio.run(agent.arun(query))
    
    for msg in trace:
        print_msg(msg)