from langchain_core.tools import Tool, tool
from dotenv import load_dotenv
import os
import requests
from tavily import TavilyClient
from rich import print

from bs4 import BeautifulSoup
from readability import Document
import re
import trafilatura

load_dotenv()
tavi = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

#if i write tool here as decorator then you can use invoke directly.
#ex: web_search.invoke("what is the capital of France?") or scrape_url.invoke("https://python.org")
@tool
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

@tool
def scrape_url(url: str) -> str:
    """
    Scrape the content of a given URL.

    Args:
        url (str): The URL to scrape.

    Returns:
        str: The scraped content.
    """
#This headers dictionary disguises your Python script as a normal web browser when it sends requests to a website.
#Without custom headers, Python libraries like requests send a default label (like python-requests/2.31.0), 
#which causes many websites to immediately block your script as an automated bot.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com"
    }

    try:
        # Send a GET request to the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html_content = response.text

        #step-1 trafilatura : 
        # it is a Python library for web scraping and text extraction. 
        # It is designed to extract meaningful content from web pages, such as articles, blog posts, and other textual information, 
        # while filtering out irrelevant elements like advertisements, navigation menus, and scripts.
        extracted_text = trafilatura.extract(html_content, include_comments=False, include_tables=False)
        if extracted_text and len(extracted_text.strip()) > 200:
            cleaned_text = re.sub(r'\s+', ' ', extracted_text)
            return cleaned_text[:5000]  # Return the first 5000 characters of the cleaned text

        #step-2 readability :
        # it is a Python library that focuses on improving the readability of web content.
        doc = Document(html_content)
        cleaned_text = doc.summary()

        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(cleaned_text, 'html.parser')

        # Remove unwanted tags like header, footer, nav, aside, form, script, and style
        for tag in soup.find_all(['header', 'footer', 'nav', 'aside', 'form', 'script', 'style']):
            tag.decompose()

        # Get text and clean it up
        text = soup.get_text(separator=' ',strip=True)
        text = re.sub(r'\s+', ' ', text)

        if text:
            return text[:5000]  # Return the first 5000 characters of the cleaned text
        return "could not extract meaningful content from the URL."

    except requests.exceptions.Timeout:
        return "[red]Request timed out while trying to scrape the URL.[/red]"

    except requests.exceptions.HTTPError as e:
        return f"[red]HTTP error occurred while scraping URL {url}: {e}[/red]"

    except Exception as e:
        return f"[red]An unexpected error occurred while scraping URL {url}: {e}[/red]"

    except requests.RequestException as e:
        return f"[red]Request error occurred while scraping URL {url}: {e}[/red]"