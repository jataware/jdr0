#!/usr/bin/env python
"""
    jdr.tools.arxiv
    
    Search and fetch arXiv papers
"""

import sys
import tempfile
import requests
from typing import Optional
from pydantic import BaseModel
from rich import print as rprint

import arxiv
from pypdf import PdfReader

from jdr.utils import disk_cache

ARXIV_SEARCH_API = "http://54.158.91.200:8000/search"

# --
# Output objects

class ArxivPaper(BaseModel):
    id       : str
    title    : str
    abstract : str
    
    def to_txt(self):
        return f"<paper>\n<id>{self.id}</id>\n<title>{self.title}</title>\n<abstract>{self.abstract}</abstract>\n</paper>"

class ArxivSearchResults(BaseModel):
    query   : str
    results : list[ArxivPaper]
    
    def to_txt(self):
        if len(self.results) == 0:
            return f"<arxiv_search_results>\n<query>{self.query}</query>\n<results>NO RESULTS FOUND - TRY ANOTHER QUERY</results>\n</arxiv_search_results>"
        
        return f"<arxiv_search_results>\n<query>{self.query}</query>\n{'\n'.join([r.to_txt() for r in self.results])}\n</arxiv_search_results>"

class ArxivPaperContent(BaseModel):
    arxiv_id : str
    title    : str
    content  : str
    
    def to_txt(self):
        return f"<arxiv_paper>\n<id>{self.arxiv_id}</id>\n<title>{self.title}</title>\n<content>{self.content}</content>\n</arxiv_paper>"

# --
# Functions

@disk_cache(cache_dir="./.cache/arxiv/search", verbose=False)
async def aarxiv_search(
    query: str, 
    limit: int = 200, 
    date_from: Optional[str] = None, 
    date_to: Optional[str] = None,
    skip_metadata: bool = True,
    _verbose: bool = True
) -> ArxivSearchResults:
    """Semantic search arXiv using custom embedding API.
    
    Args:
        query: Search query string
        limit: Maximum number of results to return
        date_from: Optional start date filter (YYYY-MM-DD)
        date_to: Optional end date filter (YYYY-MM-DD)
        skip_metadata: Whether to skip additional metadata in results
    
    Returns: ArxivSearchResults containing list of matching papers
    """
    payload = {"query": query, "top_k": int(limit * 1.5), "skip_metadata": skip_metadata}
    if date_from:
        payload["date_from"] = date_from
    if date_to:
        payload["date_to"] = date_to
    
    try:
        if _verbose:
            rprint(f"[bright_black]aarxiv_search: searching : {query}[/bright_black]", file=sys.stderr)
        
        r = requests.post(ARXIV_SEARCH_API, json=payload, timeout=60)
        r.raise_for_status()
        results = r.json().get("results", [])
        
        if _verbose:
            rprint(f"[bright_black]aarxiv_search: found {len(results)} results[/bright_black]", file=sys.stderr)
        
        # Deduplicate
        seen = set()
        unique = []
        for p in results:
            pid = p.get("id")
            if pid and pid not in seen:
                seen.add(pid)
                unique.append(p)
                if len(unique) >= limit:
                    break
        
        return ArxivSearchResults(
            query=query,
            results=[
                ArxivPaper(
                    id=p.get("id", ""),
                    title=p.get("title", ""),
                    abstract=p.get("abstract", ""),
                ) for p in unique
            ]
        )
    
    except Exception as e:
        rprint(f"[red]ERROR | aarxiv_search: {e}[/red]", file=sys.stderr)
        raise e


@disk_cache(cache_dir="./.cache/arxiv/fetch", verbose=False)
async def aarxiv_fetch(arxiv_id: str, _verbose: bool = True) -> ArxivPaperContent:
    """Fetch full paper text from arXiv PDF.
    
    Args:
        arxiv_id: The arXiv paper ID (e.g., "2301.00001" or "2301.00001v1")
    
    Returns: ArxivPaperContent with the full text extracted from the PDF
    """
    try:
        if _verbose:
            rprint(f"[bright_black]aarxiv_fetch: fetching : {arxiv_id}[/bright_black]", file=sys.stderr)
        
        # Strip version suffix if present
        clean_id = arxiv_id.split("v")[0]
        paper = next(arxiv.Client().results(arxiv.Search(id_list=[clean_id])))
        
        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = paper.download_pdf(dirpath=tmpdir)
            reader = PdfReader(pdf_path)
            content = "\n".join(page.extract_text() for page in reader.pages)
        
        if _verbose:
            rprint(f"[bright_black]aarxiv_fetch: fetched {len(content)} chars[/bright_black]", file=sys.stderr)
        
        return ArxivPaperContent(
            arxiv_id=arxiv_id,
            title=paper.title,
            content=content,
        )
    
    except Exception as e:
        rprint(f"[red]ERROR | aarxiv_fetch: {e}[/red]", file=sys.stderr)
        raise e


__all__ = ["aarxiv_search", "aarxiv_fetch"]

# --
# Test

if __name__ == "__main__":
    import asyncio
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, default="quantum machine learning")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--fetch", type=str, help="arXiv ID to fetch full text")
    args = parser.parse_args()
    
    if args.fetch:
        out = asyncio.run(aarxiv_fetch(args.fetch))
    else:
        out = asyncio.run(aarxiv_search(args.query, limit=args.limit))
    
    rprint(out)
