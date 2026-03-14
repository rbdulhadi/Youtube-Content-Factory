# YouTube Content Factory

CrewAI-powered YouTube content pipeline. Five agents, five tasks — from trend research to a complete metadata package. An end-to-end workflow for educational videos.

**Team:** Abdulhadi Rajeh, Alnahas Khaled, Abdulhadi Raja

Step-by-step build instructions (adapted for this project) are in the **[Instructions](Instructions/)** folder. Follow them in order to implement the 5-agent pipeline.

---

## Work Steps (Build the 5 Agents)

Follow the instruction phases in the table below. Each phase links to a copy-paste-ready file in this repo.

| Phase | Instruction | What to do for our 5 agents |
|-------|-------------|-----------------------------|
| **1** | [Phase_1_Intro.md](Instructions/Phase_1_Intro.md) | Understand: multi-agent system, tool use (custom + existing), MCP. Our goal: 5 agents in sequence from trend research → metadata package. |
| **2** | [Phase_2_Build_First_Crew.md](Instructions/Phase_2_Build_First_Crew.md) | **Setup:** Create/use CrewAI project. **Agents:** In `config/agents.yaml` define: Trend Scout, Creative Strategist, Scriptwriter, Visual Director, SEO Manager (roles/goals/backstories from pitch). **Tasks:** In `config/tasks.yaml` define 5 tasks (see table below), each assigned to one agent; use `context` so each task gets the previous agent’s output. **Crew:** In `crew.py` register all 5 agents and 5 tasks with `@agent` / `@task`, and create the `Crew` with sequential process. |
| **3** | [Phase_3_Tool_Calling.md](Instructions/Phase_3_Tool_Calling.md) | **Custom tool(s):** e.g. read topic or research areas from a JSON/file. Implement tool, register in `crew.py`, assign to **Trend Scout**. In `main.py` pass input (e.g. `topic`, `path`). In the Trend Scout task description, reference `{topic}` or `{path}` so the agent uses the tool. |
| **4** | [Phase_4_Web_Search_Integration.md](Instructions/Phase_4_Web_Search_Integration.md) | **Web search:** Install `crewai[tools]`, add Serper (or similar) and `SERPER_API_KEY` in `.env`. Give **Trend Scout** the web search tool so it can find the 5 most-asked questions/pain points in forums and social media. Optionally use `output_file` on tasks to save: trend list, big idea, script, storyboard, metadata (e.g. `output/trend_list.md`, `output/script.md`, etc.). |
| **5** | [Phase_5_MCP_Integration.md](Instructions/Phase_5_MCP_Integration.md) | **MCP (optional):** Add an MCP server (e.g. arXiv or YouTube) and assign its tools to an agent for extra data. |

Full index: [Instructions/README.md](Instructions/README.md).

### Task–agent mapping (from the pitch)

Task names, descriptions, and outputs below match the 5 agents in `crewai-youtube-pitch.html`.

| Step | Task (in `tasks.yaml`) | Agent | Description | Expected output |
|------|------------------------|--------|-------------|-----------------|
| 1 | `trend_scout_task` | Trend Scout | Find the 5 most-asked questions about [topic] in forums and social media. | A list of 5 concrete pain points or questions. |
| 2 | `creative_strategist_task` | Creative Strategist | Pick the best question from the scout list; develop a hook and unique angle for a ~10 min video. | A title and a “Big Idea” in 3 sentences. |
| 3 | `scriptwriter_task` | Scriptwriter | Turn the Big Idea into a structured script: intro, 3 main points, call-to-action (CTA). | A full video script. |
| 4 | `visual_director_task` | Visual Director | For each section of the script, describe what should appear on screen (e.g. B-roll, text overlays). | A visual storyboard with timestamps. |
| 5 | `seo_manager_task` | SEO Manager | Review script and storyboard; produce a CTR-optimized title, description, and 10 tags. | A complete metadata package for the video upload. |

---

## The Pipeline

| # | Agent | Role | Output |
|---|--------|------|--------|
| 01 | **Trend Scout** | Market Researcher | List of 5 concrete pain points or questions for [topic] (from forums & social) |
| 02 | **Creative Strategist** | Content Creator | Title + “Big Idea” in 3 sentences (hook & angle for a ~10 min video) |
| 03 | **Scriptwriter** | Technical Writer | Full video script (intro, 3 main points, CTA) |
| 04 | **Visual Director** | Art Director | Visual storyboard with timestamps (what appears on screen per section) |
| 05 | **SEO Manager** | Digital Growth Expert | Complete metadata package (CTR-optimized title, description, 10 tags) |

---

## Installation

Ensure you have Python >=3.10, <3.14 installed. This project uses [UV](https://docs.astral.sh/uv/) for dependency management.

1. Install uv (if needed):

```bash
pip install uv
```

2. From the project root, install dependencies:

```bash
crewai install
```

### Configuration

- **Add your `OPENAI_API_KEY`** in the `.env` file.
- Agents: `src/my_first_crew_ai_project/config/agents.yaml`
- Tasks: `src/my_first_crew_ai_project/config/tasks.yaml`
- Crew logic & tools: `src/my_first_crew_ai_project/crew.py`
- Inputs: `src/my_first_crew_ai_project/main.py`

---

## Running the Project

From the project root:

```bash
crewai run
```

This starts the YouTube Content Factory crew: agents run in sequence and produce the trend list → big idea → script → storyboard → metadata package.

---

## Understanding Your Crew

The **YouTube Content Factory** crew is made of five agents that work in sequence. Each agent consumes the previous output and produces the next artifact. Task flow and agent roles are defined in `config/tasks.yaml` and `config/agents.yaml`. The high-level idea is also described in `crewai-youtube-pitch.html`.

---

## Support

- [CrewAI documentation](https://docs.crewai.com)
- [CrewAI GitHub](https://github.com/joaomdmoura/crewai)
- [CrewAI Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with docs](https://chatg.pt/DWjSBZn)
