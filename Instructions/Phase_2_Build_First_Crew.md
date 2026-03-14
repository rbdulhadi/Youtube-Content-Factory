# Phase 2 – Build Your First Crew (YouTube Content Factory)

In this phase you create the **CrewAI multi-agent system** for the YouTube Content Factory: five agents and five tasks in sequence.

CrewAI is a framework for building collaborative AI agent systems in which multiple agents with different roles cooperate to solve complex tasks.

---

## Step 1 – Setup CrewAI Project

### 1. Use the Existing Project

This project already has a CrewAI structure. If you started from scratch you would run:

```bash
crewai create crew my_first_crew_ai_project
```

The project structure is:

```
Youtube-Content-Factory/
├── .env
├── pyproject.toml
├── README.md
├── crewai-youtube-pitch.html
├── Instructions/
└── src/
    └── my_first_crew_ai_project/
        ├── main.py
        ├── crew.py
        ├── tools/
        └── config/
            ├── agents.yaml
            └── tasks.yaml
```

### Important Project Files

| File | Purpose |
|------|--------|
| `src/my_first_crew_ai_project/main.py` | Entry point; pass inputs (e.g. `topic`) |
| `src/my_first_crew_ai_project/crew.py` | Defines the crew, agents, and tasks |
| `src/my_first_crew_ai_project/config/agents.yaml` | Defines the 5 agents |
| `src/my_first_crew_ai_project/config/tasks.yaml` | Defines the 5 tasks |
| `.env` | API keys (OPENAI_API_KEY, SERPER_API_KEY) |

### 2. Configure LLM and API Key

Edit `.env` and add:

```env
OPENAI_API_KEY=sk-....
```

During `crewai create` you may have chosen an LLM provider and model; otherwise configure the default in `crew.py` (see CrewAI/AGENTS.md).

---

## Step 2 – Create the Five Agents

Agents can be defined in **YAML** (recommended) or in Python. Use YAML for clarity.

### Edit the Agent Configuration

Open:

```
src/my_first_crew_ai_project/config/agents.yaml
```

Define these five agents (roles, goals, backstories from the pitch):

- **trend_scout** — Market Researcher: finds the 5 most-asked questions/pain points for a topic in forums and social media.  
- **creative_strategist** — Content Creator: picks the best question, develops hook and angle, outputs title + Big Idea in 3 sentences.  
- **scriptwriter** — Technical Writer: turns the Big Idea into a full script (intro, 3 points, CTA).  
- **visual_director** — Art Director: produces a visual storyboard with timestamps from the script.  
- **seo_manager** — Digital Growth Expert: produces CTR-optimized title, description, and 10 tags.

### Agent Structure (YAML)

```yaml
agent_name:
  role: >
    # role title
  goal: >
    # what this agent aims to achieve
  backstory: >
    # short backstory
```

### Copy-Paste-Ready Example (all 5 agents)

```yaml
trend_scout:
  role: >
    Market Researcher (Trend Scout)
  goal: >
    Identify the 5 most-asked questions or pain points about a given topic in forums and social media.
  backstory: >
    You are an experienced market researcher who spots what people really ask and struggle with online.

creative_strategist:
  role: >
    Content Creator (Creative Strategist)
  goal: >
    Pick the best question from the trend list and develop a hook and unique angle for a ~10 minute educational video.
  backstory: >
    You are a creative strategist who turns audience questions into compelling video concepts.

scriptwriter:
  role: >
    Technical Writer (Scriptwriter)
  goal: >
    Turn the Big Idea into a structured video script with intro, 3 main points, and a call-to-action.
  backstory: >
    You are a skilled scriptwriter who structures ideas into clear, engaging scripts.

visual_director:
  role: >
    Art Director (Visual Director)
  goal: >
    For each section of the script, describe what should appear on screen (B-roll, text overlays, etc.).
  backstory: >
    You are a visual director who translates scripts into concrete visual directions with timestamps.

seo_manager:
  role: >
    Digital Growth Expert (SEO Manager)
  goal: >
    Produce a CTR-optimized title, description, and 10 tags for the video based on script and storyboard.
  backstory: >
    You are an SEO expert who maximizes discoverability and click-through for educational content.
```

### Register Agents in `crew.py`

Open:

```
src/my_first_crew_ai_project/crew.py
```

Add an `@agent` method for each agent. **The method name must match the YAML key.**

Example:

```python
@agent
def trend_scout(self) -> Agent:
    return Agent(
        config=self.agents_config["trend_scout"],  # type: ignore[index]
        verbose=True,
    )

@agent
def creative_strategist(self) -> Agent:
    return Agent(
        config=self.agents_config["creative_strategist"],  # type: ignore[index]
        verbose=True,
    )

# ... scriptwriter, visual_director, seo_manager the same way
```

---

## Step 3 – Define the Five Tasks

Open:

```
src/my_first_crew_ai_project/config/tasks.yaml
```

Define five tasks. Each task has a **description**, **expected_output**, and **agent**. Later you will add **context** so each task receives the previous task’s output, and **output_file** to save results.

### Task Structure

```yaml
task_name:
  description: >
    # what the agent must do (use {topic} for input variable)
  expected_output: >
    # what the deliverable looks like
  agent: agent_name
```

### Copy-Paste-Ready Example (all 5 tasks)

```yaml
trend_scout_task:
  description: >
    Find the 5 most-asked questions or pain points about the topic "{topic}" in forums and social media.
    Focus on what real people ask and struggle with.
  expected_output: >
    A list of exactly 5 concrete questions or pain points, clearly numbered.
  agent: trend_scout

creative_strategist_task:
  description: >
    Using the list of 5 questions/pain points from the Trend Scout, pick the best one and develop a hook and a unique angle for a ~10 minute educational video.
    Output a title and the "Big Idea" in exactly 3 sentences.
  expected_output: >
    A video title and a "Big Idea" summarized in 3 sentences.
  agent: creative_strategist

scriptwriter_task:
  description: >
    Using the title and Big Idea from the Creative Strategist, write a full video script.
    Structure: intro, 3 main points, and a clear call-to-action (CTA) at the end.
  expected_output: >
    A complete video script with intro, 3 main sections, and CTA.
  agent: scriptwriter

visual_director_task:
  description: >
    Using the video script, describe for each section what should appear on screen (e.g. B-roll, text overlays, graphics).
    Include timestamps or section markers.
  expected_output: >
    A visual storyboard with timestamps/sections and clear descriptions of what is on screen.
  agent: visual_director

seo_manager_task:
  description: >
    Using the script and storyboard, create a metadata package for the video upload: a CTR-optimized title, a description, and 10 tags.
  expected_output: >
    A complete metadata package: title, description (2–4 sentences), and 10 tags.
  agent: seo_manager
```

### Wire Task Dependencies (context) in `crew.py`

In `crew.py`, when you define each `Task`, pass **context** so that:

- `creative_strategist_task` has `context=[self.trend_scout_task()]`
- `scriptwriter_task` has `context=[self.creative_strategist_task()]`
- `visual_director_task` has `context=[self.scriptwriter_task()]`
- `seo_manager_task` has `context=[self.visual_director_task()]`

(Phase 4 will add `output_file` to save each result to a file.)

---

## Result of Phase 2

At the end of this phase you should have:

- A working **CrewAI project** with **5 agents** and **5 tasks**
- **Sequential workflow**: Trend Scout → Creative Strategist → Scriptwriter → Visual Director → SEO Manager
- No tools yet: Trend Scout will not search the web until Phase 3 (custom tool) and Phase 4 (Serper)

Run from project root:

```bash
crewai run
```

Pass `topic` in `main.py` via `inputs = {"topic": "Your topic here"}`.
