
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from .mcp.mcp_server import get_trend_scout_tools
import os

@CrewBase
class MyYouTubeContentCreatorAiCrew:
    """My YouTube Content Creator Ai Crew"""

    agents: list[BaseAgent]
    agents_config = "config/agents.yaml"
    tasks: list[Task]
    tasks_config = "config/tasks.yaml"

    @staticmethod
    def _embedder_url() -> str:
        configured_url = os.getenv("EMBEDDING_BASE_URL")
        if configured_url:
            return configured_url
        base_url = os.getenv("BASE_URL", "http://localhost:11434").rstrip("/")
        return f"{base_url}/api/embeddings"

    local_llm = LLM(
            model=os.getenv('MODEL', 'ollama/kimi-k2.5:cloud'),
            base_url=os.getenv('BASE_URL', 'http://localhost:11434'),
            api_key=os.getenv('OLLAMA_API_KEY')
        )

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def trend_scout(self) -> Agent:
        return Agent(
            config=self.agents_config['trend_scout'], # type: ignore[index]
            llm=self.local_llm,
            tools=get_trend_scout_tools()
        )

    @agent
    def creative_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['creative_strategist'], # type: ignore[index]
            llm=self.local_llm
        )

    @agent
    def scriptwriter(self) -> Agent:
        return Agent(
            config=self.agents_config['scriptwriter'], # type: ignore[index]
            llm=self.local_llm
        )

    @agent
    def visual_director(self) -> Agent:
        return Agent(
            config=self.agents_config['visual_director'], # type: ignore[index]
            llm=self.local_llm
        )

    @agent
    def seo_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['seo_manager'], # type: ignore[index]
            llm=self.local_llm
        )


    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def trend_scout_task(self) -> Task:
        return Task(
            config=self.tasks_config['trend_scout_task'], # type: ignore[index]
            output_file='output/trend_list.md'
        )

    @task
    def creative_strategist_task(self) -> Task:
        return Task(
            config=self.tasks_config['creative_strategist_task'], # type: ignore[index]
            output_file='output/big_idea.md'
        )

    @task
    def scriptwriter_task(self) -> Task:
        return Task(
            config=self.tasks_config['scriptwriter_task'], # type: ignore[index]
            output_file='output/script.md'
        )

    @task
    def visual_director_task(self) -> Task:
        return Task(
            config=self.tasks_config['visual_director_task'], # type: ignore[index]
            output_file='output/storyboard.md'
        )

    @task
    def seo_manager_task(self) -> Task:
        return Task(
            config=self.tasks_config['seo_manager_task'], # type: ignore[index]
            output_file='output/metadata.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates My YouTube Content Creator Ai Crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        user_preference = TextFileKnowledgeSource(
            file_paths=["user_preference.txt"]
        )

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=False,
            knowledge_sources=[user_preference],
            embedder={
                "provider": "ollama",
                "config": {
                    "model_name": os.getenv("EMBEDDING_MODEL", "nomic-embed-text"),
                    "url": self._embedder_url(),
                },
            },
        )
