from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from my_project.knowledge_graph import KnowledgeGraph, save_graph_data
from my_project.tools.retrieval_tool import (
    case_retrieval_tool
)


def _persist_knowledge_graph(output) -> str:
    if output.pydantic is not None:
        save_graph_data(output.pydantic)
    elif output.json_dict:
        save_graph_data(output.json_dict)
    else:
        save_graph_data(output.raw)
    return output.raw
# Local Ollama Model

ollama_llm = LLM(
model="ollama/qwen3:4b",
base_url="http://localhost:11434"
)

@CrewBase
class MyProject:
    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def contradiction_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["contradiction_analyst"],
            llm=ollama_llm,
            verbose=True,
        )

    # ======================
    # AGENTS
    # ======================

    @agent
    def knowledge_graph_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["knowledge_graph_agent"],
            llm=ollama_llm,
            verbose=True,
        )

    @agent
    def investigator(self) -> Agent:
        return Agent(
            config=self.agents_config["investigator"],
            llm=ollama_llm,
            tools=[case_retrieval_tool],
            verbose=True,
        )

    @agent
    def defense_lawyer(self) -> Agent:
        return Agent(
            config=self.agents_config["defense_lawyer"],
            llm=ollama_llm,
            verbose=True,
        )

    @agent
    def prosecutor(self) -> Agent:
        return Agent(
            config=self.agents_config["prosecutor"],
            llm=ollama_llm,
            verbose=True,
        )

    @agent
    def judge(self) -> Agent:
        return Agent(
            config=self.agents_config["judge"],
            llm=ollama_llm,
            verbose=True,
        )

    # ======================
    # TASKS
    # ======================

    @task
    def investigation_task(self) -> Task:
        return Task(
            config=self.tasks_config["investigation_task"],
            output_file="reports/evidence_report.md",
        )

    @task
    def defense_task(self) -> Task:
        return Task(
            config=self.tasks_config["defense_task"],
            output_file="reports/defense_report.md",
        )

    @task
    def prosecution_task(self) -> Task:
        return Task(
            config=self.tasks_config["prosecution_task"],
            output_file="reports/prosecution_report.md",
        )

    @task
    def contradiction_task(self) -> Task:
        return Task(
            config=self.tasks_config["contradiction_task"],
            output_file="reports/contradiction_report.md",
        )

    @task
    def knowledge_graph_task(self) -> Task:
        return Task(
            config=self.tasks_config["knowledge_graph_task"],  # type: ignore[index]
            output_pydantic=KnowledgeGraph,
            callback=_persist_knowledge_graph,
        )

    @task
    def judgement_task(self) -> Task:
        return Task(
            config=self.tasks_config["judgement_task"],
            output_file="reports/judgement.md",
        )

    # ======================
    # CREW
    # ======================

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
