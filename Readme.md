# 🦜 LangChain Setup & Migration Guide

A practical guide for setting up the Python environment, configuring API keys, using Tavily Search, and understanding the migration from **LangChain v0.x to v1.x+**.

---

## 1. Environment Setup — Conda-Forge

If you prefer to avoid Anaconda's commercial `defaults` repository, you can configure Conda to use the community-maintained **conda-forge** channel.

### Step 1: Configure Conda Channels (Windows PowerShell)

First, inspect your current Conda configuration:

```powershell
conda config --show-sources
```

Remove the old Miniconda-level configuration file if it explicitly contains the `defaults` channel:

```powershell
Remove-Item "$env:USERPROFILE\miniconda3\.condarc" -ErrorAction SilentlyContinue
```

Configure conda-forge as your only channel by creating or updating your user-level `.condarc` file:

```powershell
@"
channels:
  - conda-forge
channel_priority: strict
"@ | Set-Content "$env:USERPROFILE\.condarc"
```

Verify the configuration:

```powershell
conda config --show channels
conda config --show-sources
```

**Expected channel configuration:**

```yaml
channels:
  - conda-forge
```

This configuration prevents Conda from falling back to the `defaults` channel. The `nodefaults` setting is generally used in individual `environment.yml` files and is not required for this global configuration.

### Step 2: Create the Python Environment

Create a dedicated environment using Python 3.11:

```powershell
conda create -n langagent python=3.11 pip -y
```

Initialize Conda for PowerShell (run this once):

```powershell
conda init powershell
```

Close and reopen PowerShell, then activate the environment:

```powershell
conda activate langagent
```

### Step 3: Install Project Dependencies

Upgrade pip and install the dependencies listed in `req.txt`:

```powershell
python -m pip install --upgrade pip
python -m pip install -r req.txt
```

---

## 2. API Key Configuration

This project can use external services for LLM inference, web search, and prompt management.

Create a `.env` file in the project root directory.

### Environment Variables

```env
# Google AI Studio - Gemini API
GOOGLE_API_KEY=your_google_ai_studio_api_key

# Tavily - Web Search
TAVILY_API_KEY=your_tavily_api_key

# LangSmith - Prompt Hub (if required)
LANGSMITH_API_KEY=your_langsmith_api_key
```

**Where to get API keys:**

| Service | Purpose | API Key |
|:---|:---|:---|
| Google AI Studio | Gemini model access | [Get API Key](https://aistudio.google.com/app/apikey) |
| Tavily | Web search and online information retrieval | [Get API Key](https://app.tavily.com/home) |
| LangSmith | Prompt Hub and prompt management | [LangSmith](https://smith.langchain.com/) |

> **Important:** Never upload your `.env` file or expose API keys in your GitHub repository. Add `.env` to your `.gitignore` file.

---

## 3. Tavily Search — Web Search Integration

**Tavily** is a useful search tool for AI agents that need to retrieve information from internet sources.

Instead of relying only on the LLM's existing knowledge, an agent can use Tavily to search for relevant online information and incorporate the returned results into its response.

### Installation

```bash
pip install -U langchain-tavily
```

### Import and Usage

```python
from langchain_tavily import TavilySearch

# Initialize the Tavily search tool
search_tool = TavilySearch(
    max_results=5,
    topic="general"
)
```

Make sure `TAVILY_API_KEY` is configured in your environment.

**Useful for:**
- Searching for up-to-date information.
- Retrieving relevant web search results.
- Supporting research-oriented AI agents.
- Providing agents with external information sources.

---

## 4. LangChain v0.x vs v1.x+ — Imports & Functions Cheat Sheet

A quick reference for understanding the important changes when migrating from **LangChain v0.x to LangChain v1.x and above**.

| Feature | Old Way — `LangChain v0.x` | New Way — `LangChain v1.x+` |
|:---|:---|:---|
| **Prompt Hub** | `from langchain import hub`<br><br>`prompt = hub.pull("hwchase17/react")` | `from langsmith import Client`<br><br>`client = Client()`<br>`prompt = client.pull_prompt("hwchase17/react")` |
| **Create Agent** | `from langgraph.prebuilt import create_react_agent` | `from langchain.agents import create_agent` |
| **Run Agent** | `agent_executor = AgentExecutor(agent=agent, tools=tools)`<br><br>`agent_executor.invoke({"input": "..."})` | **Direct agent invocation:**<br><br>`agent.invoke({`<br>&nbsp;&nbsp;`"messages": [`<br>&nbsp;&nbsp;&nbsp;&nbsp;`{"role": "user", "content": "..."}`<br>&nbsp;&nbsp;`]`<br>`})` |
| **Read Output** | `response["output"]` | `response["messages"][-1].content` |
| **Tavily Search** | `from langchain_community.tools.tavily_search import TavilySearchResults` | `from langchain_tavily import TavilySearch`<br><br>Install: `pip install -U langchain-tavily` |
| **Gemini LLM** | Provider-specific legacy implementations | `from langchain_google_genai import ChatGoogleGenerativeAI`<br><br>Install: `pip install -U langchain-google-genai` |
| **Custom Tools** | `from langchain.tools import tool` | `from langchain.tools import tool`<br><br>✅ Unchanged |

> **Note:** OpenAI (`ChatOpenAI`) and Gemini (`ChatGoogleGenerativeAI`) are different model providers, not direct version-to-version replacements.

---

## 5. Key Migration Notes

### 1. Agent Creation
The recommended agent creation API in LangChain v1.x is:

```python
from langchain.agents import create_agent
```

It replaces the older recommended `create_react_agent` approach with a more streamlined API.

### 2. Agent Execution
You no longer need to wrap the new `create_agent` result inside an `AgentExecutor`.

Instead, invoke the agent directly:

```python
response = agent.invoke({
    "messages": [
        {"role": "user", "content": "Your question here"}
    ]
})
```

### 3. Message-Based Input
The newer agent API uses a message-based structure rather than the older `input` dictionary.

### 4. Response Handling
The new agent returns a message-based state. The final assistant message can be accessed using:

```python
response["messages"][-1].content
```

### 5. Tavily Integration
Tavily now has a dedicated LangChain integration package:

```bash
pip install -U langchain-tavily
```

Use the newer import:

```python
from langchain_tavily import TavilySearch
```

### 6. Custom Tools
The `@tool` decorator import remains unchanged:

```python
from langchain.tools import tool

@tool
def example_tool(query: str) -> str:
    """An example custom tool."""
    return f"Processing: {query}"
```

### 7. Legacy Components
Some older LangChain functionality, including legacy chains and agent utilities, has moved into the `langchain-classic` package.

Install it only when your project still depends on those older components:

```bash
pip install -U langchain-classic
```

---

## 6. Useful Documentation

| Resource | Documentation |
|:---|:---|
| LangChain | [Official Documentation](https://docs.langchain.com/oss/python/langchain/overview) |
| LangChain Migration | [v1 Migration Guide](https://docs.langchain.com/oss/python/migrate/langchain-v1) |
| LangSmith | [Prompt Management](https://docs.langchain.com/langsmith/manage-prompts-programmatically) |
| Tavily | [LangChain Tavily Integration](https://github.com/tavily-ai/langchain-tavily) |
| Google Gemini | [Google AI Studio](https://aistudio.google.com/) |
| Conda-Forge | [Conda Channel Configuration](https://docs.conda.io/projects/conda/en/stable/user-guide/tasks/manage-channels.html) |

---

**Happy Building! 🚀**
