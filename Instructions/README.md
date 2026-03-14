# YouTube Content Factory — Build Instructions

Step-by-step instructions to build the 5-agent CrewAI pipeline for this project. Follow in order.

| Phase | File | Summary |
|-------|------|--------|
| **1** | [Phase_1_Intro.md](Phase_1_Intro.md) | Intro to CrewAI; project goal and technical requirements (multi-agent, tools, optional MCP). |
| **2** | [Phase_2_Build_First_Crew.md](Phase_2_Build_First_Crew.md) | Set up the project; define all 5 agents and 5 tasks; wire the crew (copy-paste-ready YAML and Python). |
| **3** | [Phase_3_Tool_Calling.md](Phase_3_Tool_Calling.md) | Custom tool: read video topic/config from JSON; assign to Trend Scout. |
| **4** | [Phase_4_Web_Search_Integration.md](Phase_4_Web_Search_Integration.md) | Add Serper web search to Trend Scout; save each task output to files. |
| **5** | [Phase_5_MCP_Integration.md](Phase_5_MCP_Integration.md) | Optional: integrate an MCP server (e.g. arXiv or YouTube) for extra data. |

The pipeline and agent roles are described in the project root in **`crewai-youtube-pitch.html`**.
