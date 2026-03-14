# Phase 3 – Tool Calling (Read Video Topic / Config)

In this phase you learn how to **create a custom tool in CrewAI** for the YouTube Content Factory.

Tools in CrewAI are **function calls that an LLM can use** to access external data or functionality.

Here, the **video topic** (and optionally other settings) will be stored in a **JSON file**. A custom tool will let the **Trend Scout** agent read this file so the crew knows which topic to research.

---

## Step 1 – Create the Input File

Create the folder `input` in the project root (if it does not exist) and add:

```
input/video_topic.json
```

Insert:

```json
{
  "topic": "How to get started with CrewAI",
  "duration_minutes": 10,
  "audience": "developers and students"
}
```

You can change `topic` to any educational video topic (e.g. "Python for beginners", "Agentic AI basics").

---

## Step 2 – Create the Tool

Create the file:

```
src/my_first_crew_ai_project/tools/read_video_topic_tool.py
```

Copy-paste-ready implementation:

```python
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import json


class ReadVideoTopicInput(BaseModel):
    """Input schema for ReadVideoTopicTool."""
    path: str = Field(..., description="Path to the video topic/config JSON file.")


class ReadVideoTopicTool(BaseTool):
    name: str = "Read Video Topic"
    description: str = (
        "Reads the video topic and optional config (duration, audience) from a JSON file. "
        "Use this to know what topic to research for the YouTube content pipeline."
    )
    args_schema: Type[BaseModel] = ReadVideoTopicInput

    def _run(self, path: str) -> str:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        topic = data.get("topic", "")
        duration = data.get("duration_minutes", 10)
        audience = data.get("audience", "")
        return (
            f"Topic: {topic}. Target duration: {duration} minutes. Audience: {audience}."
        )
```

---

## Step 3 – Register the Tool in the Crew

Open:

```
src/my_first_crew_ai_project/crew.py
```

Add the import:

```python
from my_first_crew_ai_project.tools.read_video_topic_tool import ReadVideoTopicTool
```

---

## Step 4 – Give the Tool to the Trend Scout Agent

In the **Trend Scout** agent definition, add the tool:

```python
@agent
def trend_scout(self) -> Agent:
    return Agent(
        config=self.agents_config["trend_scout"],  # type: ignore[index]
        verbose=True,
        tools=[ReadVideoTopicTool()],
    )
```

The Trend Scout can now read the video topic from the JSON file.

---

## Step 5 – Pass the Input Path When Running the Crew

Open:

```
src/my_first_crew_ai_project/main.py
```

Set the input path when kicking off the crew:

```python
inputs = {
    "path": "./input/video_topic.json",
    "topic": "How to get started with CrewAI",  # can match JSON or override
}
```

Use the same `topic` in task descriptions via `{topic}` so the agent knows what to research even if you pass it from `main.py` instead of only from the file.

---

## Step 6 – Use the Path (and Topic) in the Task Description

Open:

```
src/my_first_crew_ai_project/config/tasks.yaml
```

Make sure the Trend Scout task tells the agent to use the tool and the topic. Example:

```yaml
trend_scout_task:
  description: >
    First use the Read Video Topic tool with path "{path}" to get the video topic and audience.
    Then find the 5 most-asked questions or pain points about the topic "{topic}" in forums and social media.
    Focus on what real people ask and struggle with.
  expected_output: >
    A list of exactly 5 concrete questions or pain points, clearly numbered.
  agent: trend_scout
```

Ensure `main.py` passes both `path` and `topic` in `inputs` (e.g. read `topic` from the same JSON or pass it explicitly).

---

## Result of Phase 3

After this phase you will have:

- A **custom CrewAI tool** that reads video topic/config from a JSON file  
- The **Trend Scout** agent using this tool before researching  
- Inputs **path** and **topic** provided from `main.py` and used in the task description  

In Phase 4 you will add **web search** (Serper) to the Trend Scout so it can actually search forums and social media.

---

## What You Learned

- How **CrewAI tools** work  
- How to **create a custom tool** with an input schema  
- How to **attach a tool to an agent** and reference **inputs** in tasks  
