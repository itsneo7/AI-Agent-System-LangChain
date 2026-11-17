from src.tools.tools import web_search, scrape_url
from src.pipelines.pipeline import run_research_pip

#ot = web_search("what is the capital of France?")
#print(ot)

#ot = scrape_url.invoke("https://www.reddit.com/r/learnprogramming/.rss")
#print(ot)

topic = "what is the latest impact of ai on the job market 2026?"
ot = run_research_pip(topic)
print("\n final output: \n", ot)
