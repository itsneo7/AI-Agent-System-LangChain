from langchain.agents import create_agent
from langchain_openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools.tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(model_name="gpt-4o-mini", temperature=0)

#first agent
def the_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
    )

#sec agent
def the_scrape_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
    )
