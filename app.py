import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="AI Research Agents",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI Research Agent Dashboard")
st.caption("A multi-agent research workflow powered by LangChain.")

with st.sidebar:
    st.header("About this workflow")
    st.markdown(
        """
        The research pipeline runs through four stages:

        1. **Search Agent** – finds relevant web sources using Tavily.
        2. **Scrape Agent** – extracts useful information from those sources.
        3. **Writer Chain** – creates a structured research report.
        4. **Critic Chain** – reviews and scores the report.
        """
    )
    st.divider()
    st.caption("Make sure your API keys are configured in the root `.env` file.")

topic = st.text_area(
    "Research topic",
    placeholder="e.g. Recent advancements in autonomous mobile robots",
    height=100,
)

run_button = st.button("🚀 Run research", type="primary", use_container_width=True)

if run_button:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
        st.stop()

    # Check the keys needed by the supplied project.
    missing_keys = [
        key for key in ("GROQ_API_KEY", "TAVILY_API_KEY")
        if not os.getenv(key)
    ]
    if missing_keys:
        st.error(
            "Missing environment variable(s): "
            + ", ".join(missing_keys)
            + ". Add them to the `.env` file in the project root."
        )
        st.stop()

    # Import after loading environment variables.
    try:
        from src.agents.agents import (
            the_search_agent,
            the_scrape_agent,
            writer_chain,
            critic_chain,
        )
    except Exception as exc:
        st.exception(exc)
        st.stop()

    results = {}

    st.subheader("Live agent activity")
    progress = st.progress(0)
    status_text = st.empty()

    # Stage 1: Search
    with st.status(" Search Agent — searching the web...", expanded=True) as status:
        try:
            status_text.info("The Search Agent is looking for relevant sources.")
            search_agent = the_search_agent()
            search_response = search_agent.invoke(
                {"messages": [("user", f"Search for the topic: {topic.strip()}")]}
            )
            results["search_results"] = search_response["messages"][-1].content
            st.markdown("**Search completed.**")
            st.text_area(
                "Search agent output",
                results["search_results"],
                height=220,
                key="search_output",
            )
            status.update(label="🔎 Search Agent — completed", state="complete")
            progress.progress(25)
        except Exception as exc:
            status.update(label="🔎 Search Agent — failed", state="error")
            st.exception(exc)
            st.stop()

    # Stage 2: Scrape
    with st.status(" Scrape Agent — extracting page content...", expanded=True) as status:
        try:
            status_text.info("The Scrape Agent is processing the search results.")
            scrape_agent = the_scrape_agent()
            scrape_response = scrape_agent.invoke(
                {
                    "messages": [
                        (
                            "user",
                            "Scrape the content from the URLs in these search results. "
                            "Summarize the extracted information clearly:\n\n"
                            + results["search_results"],
                        )
                    ]
                }
            )
            results["scrape_results"] = scrape_response["messages"][-1].content
            st.markdown("**Scraping completed.**")
            st.text_area(
                "Scrape agent output",
                results["scrape_results"],
                height=260,
                key="scrape_output",
            )
            status.update(label=" Scrape Agent — completed", state="complete")
            progress.progress(50)
        except Exception as exc:
            status.update(label=" Scrape Agent — failed", state="error")
            st.exception(exc)
            st.stop()

    # Stage 3: Writer
    with st.status(" Writer Chain — preparing the report...", expanded=True) as status:
        try:
            status_text.info("The Writer Chain is creating the research report.")
            combined_research = (
                f"Search results:\n{results['search_results']}\n\n"
                f"Extracted research:\n{results['scrape_results']}"
            )
            results["research_report"] = writer_chain.invoke(
                {"topic": topic.strip(), "research": combined_research}
            )
            st.markdown("**Draft report generated.**")
            status.update(label=" Writer Chain — completed", state="complete")
            progress.progress(75)
        except Exception as exc:
            status.update(label=" Writer Chain — failed", state="error")
            st.exception(exc)
            st.stop()

    # Stage 4: Critic
    with st.status(" Critic Chain — reviewing the report...", expanded=True) as status:
        try:
            status_text.info("The Critic Chain is evaluating the report.")
            results["critic_report"] = critic_chain.invoke(
                {"report": results["research_report"]}
            )
            st.markdown("**Review completed.**")
            status.update(label=" Critic Chain — completed", state="complete")
            progress.progress(100)
            status_text.success("All stages completed successfully.")
        except Exception as exc:
            status.update(label=" Critic Chain — failed", state="error")
            st.exception(exc)
            st.stop()

    st.divider()
    st.subheader(" Final outputs")

    report_tab, critic_tab, search_tab, scrape_tab = st.tabs(
        ["Research report", "Critic review", "Search results", "Scraped research"]
    )

    with report_tab:
        st.markdown(results["research_report"])
        st.download_button(
            " Download research report",
            data=results["research_report"],
            file_name="research_report.md",
            mime="text/markdown",
        )

    with critic_tab:
        st.markdown(results["critic_report"])

    with search_tab:
        st.text(results["search_results"])

    with scrape_tab:
        st.text(results["scrape_results"])

else:
    st.info("Enter a topic above and click **Run research** to watch each agent work.")
