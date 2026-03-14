# Intro to CrewAI Framework — YouTube Content Factory

~ 30 minutes.

More info: https://crewai.com/

---

# Assignment: AI Agent System for YouTube Content Pipeline

## Objective

The goal of this project is to build an **AI agent system using CrewAI** that produces a full **YouTube content package** for educational videos: from trend research to a ready-to-upload metadata bundle.

CrewAI is a framework for building collaborative AI agent systems in which specialized agents work together to solve complex tasks.

---

# Pipeline (5 Agents, 5 Tasks)

## 1. Trend Research

The **Trend Scout** agent finds the **5 most-asked questions or pain points** about a given topic in forums and social media.

Output: a list of 5 concrete questions or pain points.

## 2. Creative Strategy

The **Creative Strategist** agent picks the best question from that list and develops a **hook** and unique **angle** for a ~10 minute video.

Output: a title and a “Big Idea” in 3 sentences.

## 3. Script Writing

The **Scriptwriter** agent turns the Big Idea into a **structured video script**: intro, 3 main points, and a call-to-action (CTA).

Output: a full video script.

## 4. Visual Storyboard

The **Visual Director** agent reads the script and describes **what should appear on screen** for each section (e.g. B-roll, text overlays).

Output: a visual storyboard with timestamps.

## 5. SEO & Metadata

The **SEO Manager** agent reviews script and storyboard and produces a **CTR-optimized title, description, and 10 tags** for the video upload.

Output: a complete metadata package.

---

# Technical Requirements

The implementation should demonstrate the following.

## 1. Multi-Agent System

The system must use **CrewAI** with **five agents** that collaborate in sequence.

In CrewAI, agents are autonomous entities with specific roles and goals that perform tasks in a workflow. Each agent consumes the previous agent’s output.

## 2. Tool Use

The system must use **tools with agents**.

Tools extend agents with actions such as web search, API calls, or file/JSON reading.

This includes:

### Custom Tools

Implement **at least one custom tool**, for example:

- reading the video topic or config from a JSON file  
- reading from a text file  
- any other small helper (e.g. format validation)

### Existing Tools

Integrate at least one **existing CrewAI tool**, such as:

- **Serper.dev** (https://serper.dev) for web search (used by the Trend Scout to find questions in forums and social media).

## 3. MCP Integration (Optional)

The system can optionally demonstrate **MCP (Model Context Protocol)** integration.

MCP lets agents talk to external tools and services through a standard interface (e.g. YouTube search, other APIs).

---

# What You Will Build

By the end of the instructions (Phases 2–5) you will have:

- A **CrewAI project** with 5 agents and 5 tasks in sequence.  
- **Trend Scout** using a custom tool (e.g. read topic/config) and web search (Serper).  
- **Creative Strategist**, **Scriptwriter**, **Visual Director**, **SEO Manager** using context from the previous task.  
- Optional **MCP** integration for extra data sources.  
- Outputs written to files (e.g. `output/trend_list.md`, `output/big_idea.md`, `output/script.md`, `output/storyboard.md`, `output/metadata.md`).

Reference: project idea and agent roles are described in **`crewai-youtube-pitch.html`** in the project root.
