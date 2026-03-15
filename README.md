# YouTube Content Factory

CrewAI-powered YouTube content pipeline. Five agents, five tasks — from trend research to a complete metadata package. An end-to-end workflow for educational videos.

**Team:** Abdulhadi Rajeh, Alnahas Khaled, Abdulhadi Raja

---

## 🚀 Setup from Scratch

Follow these steps to get the YouTube Content Factory running on your local machine.

### 1. Prerequisites
- **Python:** 3.10, 3.11, or 3.12
- **UV:** Fast Python package installer and resolver.
  ```bash
  pip install uv
  ```
- **Ollama:** Running locally for LLM and Embeddings.

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

2. **Install dependencies using CrewAI CLI:**
   ```bash
   crewai install
   ```

### 4. Configuration (.env)

Create a `.env` file in the project root (or update the existing one) with the following variables:

```env
# LLM Configuration
MODEL=ollama/kimi-k2.5:cloud
BASE_URL=http://localhost:11434
OLLAMA_API_KEY=NA  # Set to NA for local Ollama usage

# Embedding Configuration
EMBEDDING_MODEL=nomic-embed-text

# Tools Configuration
YOUTUBE_API_KEY=your_youtube_api_key_here
ENABLE_MCP_TOOLS=true
CREWAI_TRACING_ENABLED=true

# Optional: If you want to use OpenAI instead
# OPENAI_API_KEY=sk-...
```

---

## 🛠 Tools Used

The crew leverages several powerful tools to automate the research and content creation process:

1.  **ScrapeWebsiteTool (CrewAI Native):** Used by the **Trend Scout** to read content from forums and social media pages.
2.  **MCP YouTube Tools:**
    - Integrated via `MCPServerAdapter`.
    - Allows the agents to search for trending videos and analyze successful content patterns directly on YouTube.
    - Requires `mcp-youtube` to be installed: `uv tool install git+https://github.com/sparfenyuk/mcp-youtube`.
3.  **RAG Tool (Custom Ollama RAG):**
    - A custom RAG (Retrieval-Augmented Generation) tool configured to work with the local Ollama instance for script research and user preference grounding.

---

## 🤖 The Pipeline

The **YouTube Content Factory** consists of five specialized agents working in a sequential process:

| # | Agent | Role | Output |
|---|--------|------|--------|
| 01 | **Trend Scout** | Market Researcher | List of 5 concrete pain points or questions for [topic] (from forums & social) |
| 02 | **Creative Strategist** | Content Creator | Title + “Big Idea” in 3 sentences (hook & angle for a ~10 min video) |
| 03 | **Scriptwriter** | Technical Writer | Full video script (intro, 3 main points, CTA) |
| 04 | **Visual Director** | Art Director | Visual storyboard with timestamps (what appears on screen per section) |
| 05 | **SEO Manager** | Digital Growth Expert | Complete metadata package (CTR-optimized title, description, 10 tags) |

---

## 🏃 Running the Project

From the project root:

```bash
crewai run
```

This starts the pipeline: agents run in sequence and produce artifacts in the `output/` directory (e.g., `trend_list.md`, `script.md`, `metadata.md`).

---

## 📂 Project Structure

- `src/my_first_crew_ai_project/config/agents.yaml`: Agent definitions.
- `src/my_first_crew_ai_project/config/tasks.yaml`: Task definitions.
- `src/my_first_crew_ai_project/crew.py`: Crew orchestration and tool registration.
- `src/my_first_crew_ai_project/main.py`: Entry point and inputs.
- `src/my_first_crew_ai_project/mcp/`: MCP server integration.
- `src/my_first_crew_ai_project/rag/`: RAG and Ollama configuration.

---

## 🤝 Support

- [CrewAI documentation](https://docs.crewai.com)
- [Ollama documentation](https://github.com/ollama/ollama)
