from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

from zlamida_core.core.factory import AgentFactory
from zlamida_core.core.memory import ConvoGraph
from zlamida_core.core.log import get_logger

app = FastAPI()

graph = ConvoGraph(Path("convo_graph.json"))
logger = get_logger(__name__)


class Task(BaseModel):
    text: str


@app.post("/run/{agent_name}")
async def run_agent(agent_name: str, task: Task) -> dict:
    agent = AgentFactory.create(agent_name, agent_name, memory_path=graph.path)
    result = agent.run(task.text)
    graph.append({"agent": agent.name, "task": task.text, "result": result})
    logger.info("%s -> %s", agent.name, result)
    return {"result": result}


@app.get("/history")
async def history() -> list[dict]:
    logger.info("History requested")
    return graph.all()

