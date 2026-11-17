from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools.tools import web_search, scrape_url
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

load_dotenv()


llm = ChatGroq(model="openai/gpt-oss-120b")



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

#An LCEL (LangChain Expression Language) chain is a declarative way to link together AI 
# components—such as prompt templates, language models, retrievers, and output parsers—using
# Python's pipe operator (|).
#Instead of writing complex, imperative Python code for each step of a workflow, 
# you stack modular building blocks sequentially:
#chain = prompt | model | output_parser

#writer chain
writer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that writes content based on user input."),
        ("human", """ write a  detailed research report on  the topic belo.
    
    Topic: {topic}
    Research: {research}
    
    structure the report with an introduction, main body, and conclusion.
    be detailed,factual, and proffesional.
    """),
    ]
)

writer_chain = writer_prompt | llm | StrOutputParser()

critic_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that critiques content based on user input."),
        ("human", """ critique the research report below.
    
    Research Report: {report}

    score the report on a scale of 1 to 10, with 10 being the highest quality.

    strengths: provide constructive feedback, highlight strengths and weaknesses, and suggest improvements.

    one line summary: provide a concise summary of the overall quality and effectiveness of the report.
    """),
    ]
)

critic_chain = critic_prompt | llm | StrOutputParser()