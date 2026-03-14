# Phase 5 – MCP Integration (Optional)

In this phase you can add an **MCP (Model Context Protocol) server** to your CrewAI system so agents can use **external tools** (e.g. YouTube search, arXiv, or other APIs) through a standard interface.

For the YouTube Content Factory, MCP is **optional**. Use it if you want, for example:

- **YouTube search** (e.g. find similar videos, trending titles)  
- **arXiv** or other research sources  
- Any other MCP-compatible server  

The steps below use the **arXiv MCP server** as a copy-paste-ready example; you can swap it for another MCP server (e.g. YouTube) if available.

---

## Step 1 – Preparation

Install MCP support for CrewAI:

```bash
uv add crewai-tools[mcp]
```

Example: install the arXiv MCP server (optional for this project):

```bash
uv tool install arxiv-mcp-server
```

https://pypi.org/project/arxiv-mcp-server/

---

## Step 2 – Create MCP Folder and Server Adapter

Create a folder next to `tools`:

```
src/my_first_crew_ai_project/mcp/
```

Create the file:

```
src/my_first_crew_ai_project/mcp/mcp_server.py
```

Copy-paste-ready example (arXiv; replace with your MCP server if different):

```python
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters


def get_mcp_tools():
    server_params = [
        StdioServerParameters(
            command="uv",
            args=[
                "tool",
                "run",
                "arxiv-mcp-server",
                "--storage-path",
                "./papers",
            ],
        )
        # Add more MCP servers here if needed (e.g. YouTube search server)
    ]
    adapter = MCPServerAdapter(server_params)
    return adapter.tools
```

If you use another MCP server, change `command` and `args` to match that server’s invocation.

---

## Step 3 – Import and Load MCP Tools in `crew.py`

Open:

```
src/my_first_crew_ai_project/crew.py
```

Add imports:

```python
from my_first_crew_ai_project.mcp.mcp_server import get_mcp_tools
```

Load the tools (e.g. at the top of the crew class or in a method):

```python
mcp_tools = get_mcp_tools()
```

---

## Step 4 – Assign MCP Tools to an Agent

You can either:

- **Option A:** Give MCP tools to the **Trend Scout** (e.g. to search arXiv or another source in addition to Serper), or  
- **Option B:** Add a **sixth agent** (e.g. “Research Librarian”) that only does MCP-based search and passes results to the Trend Scout or Creative Strategist.

**Option A – Trend Scout uses MCP as well:**

```python
@agent
def trend_scout(self) -> Agent:
    return Agent(
        config=self.agents_config["trend_scout"],  # type: ignore[index]
        verbose=True,
        tools=[ReadVideoTopicTool(), SerperDevTool(), *get_mcp_tools()],
    )
```

**Option B – New agent (e.g. Librarian) with its own task:**

In `config/agents.yaml` add:

```yaml
librarian:
  role: >
    Research Librarian
  goal: >
    Find relevant papers or resources for the video topic using external sources.
  backstory: >
    You are an experienced researcher who finds high-quality references and similar content.
```

In `config/tasks.yaml` add a task that runs after the trend list (or after the big idea) and give it **context** from the previous task. Then in `crew.py` add the agent and task and give it `tools=get_mcp_tools()`.

For a **minimal YouTube Content Factory**, you can **skip Phase 5** and still meet the project goal with 5 agents, custom tool, and Serper.

---

## Step 5 – Run and Verify

From the project root:

```bash
crewai run
```

If the MCP server is configured, the agent that has MCP tools will be able to call them (e.g. search arXiv). Check the agent’s verbose output to confirm.

---

## Result of Phase 5

- **MCP** integrated so agents can call external MCP tools  
- Either the Trend Scout or a dedicated agent uses MCP for extra data (e.g. papers, YouTube)  
- Optional: extend the pipeline with more MCP servers or agents  

---

## What You Learned

- How **MCP servers** work with CrewAI  
- How to **expose MCP tools** via an adapter and assign them to agents  
- How to **optionally extend** the YouTube Content Factory with external APIs  
