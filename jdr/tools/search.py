#!/usr/bin/env python
"""
    jdr.tools.search
    
    Search the web
"""

import os
import sys
import httpx
import asyncio
from pydantic import BaseModel
from rich import print as rprint

from jdr.utils import disk_cache

# --
# Output object

class SearchResult(BaseModel):
    # [TODO] return more fields?
    
    title   : str
    url     : str
    content : str
    
    def to_txt(self):
        # [TODO] fancier formatting?
        return f"<result>\n<title>{self.title}</title>\n<url>{self.url}</url>\n<content>{self.content}</content>\n</result>"

class SearchResults(BaseModel):
    query   : str
    results : list[SearchResult]
    
    def to_txt(self):
        if len(self.results) == 0:
            return f"<search_results>\n<query>{self.query}</query>\n<results>NO RESULTS FOUND - TRY ANOTHER QUERY</results>\n</search_results>"
            
        return f"<search_results>\n<query>{self.query}</query>\n{'\n'.join([result.to_txt() for result in self.results])}\n</search_results>"

class MultiSearchResults(BaseModel):
    results : list[SearchResults]
    
    def to_txt(self):
        return '\n\n'.join([result.to_txt() for result in self.results])

# --
# Functions

@disk_cache(cache_dir="./.cache/search/serp", verbose=False)
async def asearch_serp(query:str, engine:str = "google", _verbose:bool = True) -> str:
    """ Use a search engine to search for a single query """
    # [TODO] expose more parameters?
    
    assert isinstance(query, str)
    assert isinstance(engine, str)
    
    API_KEY = os.environ.get("SERPAPI_API_KEY")
    if not API_KEY:
        raise Exception("SERPAPI_API_KEY is not set")

    url    = "https://serpapi.com/search.json"
    params = {"q": query, "api_key": API_KEY, "engine": engine}
    
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            if _verbose:
                rprint(f"[bright_black]asearch_serp: fetching : {query}[/bright_black]", file=sys.stderr)
            res = await client.get(url, params=params)
            if _verbose:
                rprint(f"[bright_black]asearch_serp: fetched  : {query}[/bright_black]", file=sys.stderr)

            if res.status_code != 200:
                rprint(f"[red]ERROR | search_serp: status_code != 200 - {res.status_code}[/red]", file=sys.stderr)
                raise Exception(f"ERROR | search_serp: status_code != 200 - {res.status_code}")
            
            data = res.json()
            if not data:
                rprint(f"[yellow]WARNING | search_serp: data is None[/yellow]", file=sys.stderr)
                return SearchResults(query=query, results=[])
            
            if 'organic_results' not in data:
                rprint(f"[yellow]WARNING | search_serp: organic_results not in data[/yellow]", file=sys.stderr)
                return SearchResults(query=query, results=[])
            
            return SearchResults(
                query   = query,
                results = [
                    SearchResult(
                        title   = result["title"],
                        url     = result["link"],
                        content = result.get("snippet", "<missing>"),    
                    ) for result in data["organic_results"] # [TODO] idk about this
                ]
            )

    except Exception as e:
        rprint(f"[red]ERROR | search_serp: {e}[/red]", file=sys.stderr)
        raise e

@disk_cache(cache_dir="./.cache/search/serp_multi", verbose=False)
async def asearch_serp_multi(queries:list[str], engine:str = "google") -> str:
    """ Use a search engine to search for multiple queries """
        
    tasks = []
    for i, query in enumerate(queries):
        rprint(f"[bright_black]asearch_serp_multi - QUERY[{i}/{len(queries)}]: {query}[/bright_black]", file=sys.stderr)
        tasks.append(asearch_serp(query, engine, _verbose=False))
    
    return MultiSearchResults(
        results = await asyncio.gather(*tasks),
    )

__all__ = ["asearch_serp", "asearch_serp_multi"]

# --
# Test

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, default="quantum computing")
    parser.add_argument("--engine", type=str, default="google")
    args = parser.parse_args()  
    
    out = asyncio.run(asearch_serp(args.query, engine=args.engine))
    rprint(out)

