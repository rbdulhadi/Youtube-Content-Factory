# YouTube Content Factory

CrewAI-powered YouTube content pipeline. Five agents, five tasks — from trend research to a complete metadata package. An end-to-end workflow for educational videos.

**Team:** Abdulhadi Rajeh, Alnahas Khaled, Abdulhadi Raja

---

## 🚀 Setup from Scratch

Follow these steps to get the YouTube Content Factory running on your local machine.

### 1. Prerequisites
- **Python:** 3.10, 3.11, 3.12, or 3.13 (see `pyproject.toml`)
- **UV:** Fast Python package installer and resolver (recommended).
  ```bash
  pip install uv
  ```
- **Ollama:** Running locally for LLM and embeddings.

### 2. Local LLM Setup (Ollama)
This project is configured to use **Ollama** for both the LLM and the embedding model to ensure privacy and low cost.

1. **Install Ollama:** Download and install from [ollama.com](https://ollama.com/).
2. **Pull the required models:**
   ```bash
   # Pull the LLM (Kimi-k2.5 cloud version via Ollama)
   ollama pull kimi-k2.5:cloud

   # Pull the Embedding model
   ollama pull nomic-embed-text
   ```
3. **Ensure Ollama is running:** The API is usually available at `http://localhost:11434`.

### 3. Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Youtube-Content-Factory
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```
   Or use the CrewAI CLI: `crewai install`

### 4. Configuration (.env)

Create a `.env` file in the project root (or update the existing one) with the following variables:

```env
# LLM Configuration
MODEL=ollama/kimi-k2.5:cloud
BASE_URL=http://localhost:11434
OLLAMA_API_KEY=NA  # Set to NA for local Ollama usage

# Embedding Configuration
EMBEDDING_MODEL=nomic-embed-text

# Tools & MCP
YOUTUBE_API_KEY=your_youtube_api_key_here
MCP_ENABLED=true
CREWAI_TRACING_ENABLED=true

# Optional: If you want to use OpenAI instead
# OPENAI_API_KEY=sk-...
```

---

## 🛠 Tools & Knowledge

The crew uses the following tools and knowledge sources:

1.  **ScrapeWebsiteTool (CrewAI):** Used by the **Trend Scout** to read content from forums and social media (one URL per call).
2.  **MCP tools (Trend Scout):**
    - **YouTube MCP server** — search trending videos and analyze content patterns. Requires `YOUTUBE_API_KEY` and:  
      `uv tool install git+https://github.com/sparfenyuk/mcp-youtube`
    - **Local MCP server** (`mcp/local_mcp_server.py`) — project info and video metrics (e.g. engagement rate). No extra install.
3.  **Crew knowledge:** `knowledge/user_preference.txt` is loaded as a **TextFileKnowledgeSource** so all agents can use viewer preferences (e.g. name, interests, location). Embeddings use the Ollama embedder (`nomic-embed-text`) when knowledge is queried.

---

## 🤖 The Pipeline

The **YouTube Content Factory** consists of five specialized agents working in a sequential process:

| # | Agent | Role | Output |
|---|--------|------|--------|
| 01 | **Trend Scout** | Market Researcher | List of 5 concrete pain points or questions for [topic] (from forums & social) |
| 02 | **Creative Strategist** | Content Creator | Title + “Big Idea” in 3 sentences (hook & angle for a ~15 min video) |
| 03 | **Scriptwriter** | Technical Writer | Full video script (intro, 3 main points, CTA; ~15 min) |
| 04 | **Visual Director** | Art Director | Visual storyboard with timestamps (what appears on screen per section) |
| 05 | **SEO Manager** | Digital Growth Expert | Complete metadata package (CTR-optimized title, description, 10 tags) |

---

## 🏃 Running the Project

From the project root:

```bash
crewai run
```

This starts the pipeline: agents run in sequence and produce artifacts in the `output/` directory: `trend_list.md`, `big_idea.md`, `script.md`, `storyboard.md`, `metadata.md`. Default topic in `main.py` is "Sourdough and Pizza Baking"; change the `topic` in `run()` to try other subjects.

---

## 📂 Project Structure

- `src/my_first_crew_ai_project/config/agents.yaml` — Agent definitions (roles, goals, backstories).
- `src/my_first_crew_ai_project/config/tasks.yaml` — Task definitions and dependencies.
- `src/my_first_crew_ai_project/crew.py` — Crew class `MyYouTubeContentCreatorAiCrew`, tool wiring, and Ollama LLM/embedder.
- `src/my_first_crew_ai_project/main.py` — Entry point (`run()`, `train()`, `test()`, `replay()`, `run_with_trigger()`).
- `src/my_first_crew_ai_project/mcp/` — MCP integration: `mcp_server.py` (YouTube + local MCP), `local_mcp_server.py` (project info, video metrics).
- `knowledge/user_preference.txt` — Crew knowledge source (viewer preferences) used by all agents.

---

## 🤝 Support

- [CrewAI documentation](https://docs.crewai.com)
- [Ollama documentation](https://github.com/ollama/ollama)
