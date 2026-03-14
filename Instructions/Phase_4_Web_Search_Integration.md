# Phase 4 – Web Search Integration (Serper)

In this phase you integrate an **existing web search tool** (Serper) so the **Trend Scout** can perform real searches for questions and pain points in forums and social media.

CrewAI tools: https://docs.crewai.com/en/tools/overview

---

## Step 0 – Prerequisites

Install the CrewAI tools package:

```bash
uv add crewai-tools
```

Or:

```bash
pip install "crewai[tools]"
```

In your crew code, import the web search tool:

```python
from crewai_tools import SerperDevTool
```

---

## Step 1 – Create a Serper API Key

1. Register at https://serper.dev  
2. Create an API key.  
3. Add it to `.env`:

```env
SERPER_API_KEY=your_api_key_here
```

---

## Step 2 – Add the Web Search Tool to the Trend Scout

Open:

```
src/my_first_crew_ai_project/crew.py
```

Add Serper to the **Trend Scout** agent (together with your custom tool):

```python
from crewai_tools import SerperDevTool
from my_first_crew_ai_project.tools.read_video_topic_tool import ReadVideoTopicTool

# ...

@agent
def trend_scout(self) -> Agent:
    return Agent(
        config=self.agents_config["trend_scout"],  # type: ignore[index]
        verbose=True,
        tools=[ReadVideoTopicTool(), SerperDevTool()],
    )
```

The Trend Scout can now:

- Read the video topic from the JSON file  
- Perform web searches to find real questions and pain points in forums and social media  

---

## Step 3 – Update the Trend Scout Task Description (Optional)

In `config/tasks.yaml` you can make the instruction to search the web explicit:

```yaml
trend_scout_task:
  description: >
    First use the Read Video Topic tool with path "{path}" to get the video topic.
    Then use web search to find the 5 most-asked questions or pain points about "{topic}" in forums, Reddit, Quora, and social media.
    Focus on what real people ask and struggle with. The current year is {current_year}.
  expected_output: >
    A list of exactly 5 concrete questions or pain points, clearly numbered.
  agent: trend_scout
```

If you use `{current_year}` in the description, pass it in `main.py`: `inputs["current_year"] = str(datetime.now().year)`.

---

## Step 4 – Save Each Task Output to a File

So you get copy-paste-ready artifacts, save each agent’s output to a file. In `crew.py`, when defining each task, add `output_file`:

```python
@task
def trend_scout_task(self) -> Task:
    return Task(
        config=self.tasks_config["trend_scout_task"],  # type: ignore[index]
        context=[],
        output_file="output/trend_list.md",
    )

@task
def creative_strategist_task(self) -> Task:
    return Task(
        config=self.tasks_config["creative_strategist_task"],  # type: ignore[index]
        context=[self.trend_scout_task()],
        output_file="output/big_idea.md",
    )

@task
def scriptwriter_task(self) -> Task:
    return Task(
        config=self.tasks_config["scriptwriter_task"],  # type: ignore[index]
        context=[self.creative_strategist_task()],
        output_file="output/script.md",
    )

@task
def visual_director_task(self) -> Task:
    return Task(
        config=self.tasks_config["visual_director_task"],  # type: ignore[index]
        context=[self.scriptwriter_task()],
        output_file="output/storyboard.md",
    )

@task
def seo_manager_task(self) -> Task:
    return Task(
        config=self.tasks_config["seo_manager_task"],  # type: ignore[index]
        context=[self.visual_director_task()],
        output_file="output/metadata.md",
    )
```

Create an `output` folder in the project root if it does not exist (CrewAI may create it when `output_file` is set, depending on version).

---

## Result of Phase 4

After this phase you will have:

- The **Trend Scout** using **Serper** for real web search**  
- All five agents running in sequence with **context** and **output_file**  
- Generated files:  
  - `output/trend_list.md`  
  - `output/big_idea.md`  
  - `output/script.md`  
  - `output/storyboard.md`  
  - `output/metadata.md`  

---

## What You Learned

- How to **integrate an existing CrewAI tool** (Serper)  
- How to **combine a custom tool and web search** in one agent  
- How to **save each task result to a file** with `output_file`  
