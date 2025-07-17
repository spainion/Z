from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

from zlamida_core.core.factory import AgentFactory
from zlamida_core.core.memory import ConvoGraph

app = FastAPI()

graph = ConvoGraph(Path("convo_graph.json"))


class Task(BaseModel):
    text: str


@app.post("/run/{agent_name}")
async def run_agent(agent_name: str, task: Task) -> dict:
    agent = AgentFactory.create(agent_name, agent_name)
    result = agent.run(task.text)
    graph.append({"agent": agent.name, "task": task.text, "result": result})
    return {"result": result}


@app.get("/history")
async def history() -> list[dict]:
    return graph.all()

