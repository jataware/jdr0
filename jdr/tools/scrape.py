#!/usr/bin/env python
"""
    jdr.tools.scrape
    
    Scrape a webpage
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

class ScrapeResult(BaseModel):
    title       : str
    description : str
    url         : str
    content     : str
    
    def to_txt(self):
        # [TODO] fancier formatting?
        return f"<scrape_result>\n<title>{self.title}</title>\n<description>{self.description}</description>\n<url>{self.url}</url>\n<content>{self.content}</content>\n</scrape_result>"


# --
# Functions

@disk_cache(cache_dir="./.cache/scrape/jina", verbose=False)
async def ascrape_jina(url: str, _verbose: bool = True) -> str:
    """ Download a webpage """
    
    API_KEY = os.environ.get("JINA_API_KEY")
    if not API_KEY:
        raise Exception("JINA_API_KEY is not set")
    
    url     = f"https://r.jina.ai/{url}"

    headers = {
        "Accept"          : "application/json",
        "Authorization"   : f"Bearer {API_KEY}",
        "X-Engine"        : "browser",
        "X-Return-Format" : "markdown",
        "X-Token-Budget"  : "1000000" #  very high limit
    }
    
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            if _verbose:
                rprint(f"[bright_black]ascrape_jina: fetching : {url}[/bright_black]", file=sys.stderr)
            res = await client.get(url, headers=headers)
            if _verbose:
                rprint(f"[bright_black]ascrape_jina: fetched  : {url}[/bright_black]", file=sys.stderr)
            
            if res.status_code != 200:
                rprint(f"[red]ERROR | scrape_jina: status_code != 200 - {res.status_code}[/red]", file=sys.stderr)
                raise Exception(f"ERROR | scrape_jina: status_code != 200 - {res.status_code}")
            
            data = res.json().get("data", None)
            if not data:
                rprint(f"[red]WARNING | scrape_jina: results is None[/red]", file=sys.stderr)
                raise Exception("ERROR | scrape_jina: results is None")
            
            return ScrapeResult(
                title       = data["title"],
                description = data["description"],
                url         = data["url"],
                content     = data["content"],
            )
    
    except Exception as e:
        rprint(f"[red]ERROR | scrape_jina: {e}[/red]", file=sys.stderr)
        raise e


__all__ = ["ascrape_jina"]

# --
# Test

if __name__ == "__main__":
    out = asyncio.run(ascrape_jina("https://nyt.com"))
    rprint(out)