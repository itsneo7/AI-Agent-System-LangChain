from langchain_core.tools import Tool
from dotenv import load_dotenv
import os
import requests
from tavily import TavilyClient
from rich import print

load_dotenv()
tavi = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def web_search(query: str) -> str:
    """
    Perform a web search using Tavily API.

    Args:
        query (str): The search query.

    Returns:
        str: The search results.
    """
    response = tavi.search(query=query,max_results=5)

    out = []

    for r in response["results"]:
        out.append(
            f"[bold blue]{r['title']}[/bold blue]\n{r['url']}\nsnippet: {r['content'][:300]}\n")

    return "\n".join(out)
