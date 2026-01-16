"""Analyst module for deep reading and content extraction."""

import asyncio
import logging
from typing import Optional

import aiohttp
from bs4 import BeautifulSoup
from langchain_core.runnables import RunnableConfig
from markdownify import markdownify as md

from Artistic_DeepResearch.configuration import Configuration

async def deep_read_url(url: str, config: RunnableConfig = None) -> str:
    """Fetch and extract clean markdown content from a URL.
    
    Args:
        url: The URL to fetch.
        config: Configuration object.
        
    Returns:
        Cleaned markdown content or error message.
    """
    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                "User-Agent": "ArtisticDeepResearch/1.0 (Research Agent; +https://artisticimpression.org)"
            }
            async with session.get(url, headers=headers, timeout=15) as response:
                if response.status != 200:
                    return f"Error reading {url}: Status {response.status}"
                
                html = await response.text()
                
                # Parse HTML
                soup = BeautifulSoup(html, 'html.parser')
                
                # Remove unwanted elements
                for script in soup(["script", "style", "nav", "footer", "iframe"]):
                    script.decompose()
                    
                # Convert to Markdown
                markdown = md(str(soup), heading_style="ATX")
                
                # Simple cleanup
                lines = [line.strip() for line in markdown.splitlines() if line.strip()]
                clean_text = "\n".join(lines)
                
                return clean_text[:50000] # Limit content length
                
    except Exception as e:
        return f"Error reading {url}: {str(e)}"

async def analyze_urls(urls: list[str], config: RunnableConfig) -> dict[str, str]:
    """Analyze multiple URLs in parallel."""
    tasks = [deep_read_url(url, config) for url in urls]
    results = await asyncio.gather(*tasks)
    return dict(zip(urls, results))
