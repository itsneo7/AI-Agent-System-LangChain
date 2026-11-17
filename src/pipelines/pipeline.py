from src.agents.agents import the_search_agent, the_scrape_agent, writer_chain, critic_prompt

def run_research_pip(topic : str) -> dict:

    state = {}

    #search agent working
    print("\n"+" ="*50)
    print("search agent is working ")
    print(" ="*50)

    search_agent = the_search_agent()
    search_res = search_agent.invoke({
        "messages" : [("user", f"search for the topic: {topic}")]
    })

    state["search_results"] = search_res['messages'][-1].content
    print("\n search results: \n", state["search_results"])

    #reader agent working
    print("\n"+" ="*50)
    print("scrape agent is working ")
    print(" ="*50)

    scrape_agent = the_scrape_agent()
    scrape_res = scrape_agent.invoke({
        "messages" : [("user", f"scrape the content of the following search results: {state['search_results']}")]
    })
    state["scrape_results"] = scrape_res['messages'][-1].content
    print("\n scrape results: \n", state["scrape_results"])

    #writer chain working
    print("\n"+" ="*50)
    print("writer chain is working ")
    print(" ="*50)

    research_combined = (
        f"search results: \n {state['search_results']}\n\n"
        f"detailed search results: {state['scrape_results']}"
    )

    state["research_report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\n research report: \n", state["research_report"])\

    #critic report
    print("\n"+" ="*50)
    print("critic report is working ")
    print(" ="*50)

    state["critic_report"] = critic_prompt.invoke({
        "report": state["research_report"]
    })

    print("\n critic report: \n", state["critic_report"])

    return state