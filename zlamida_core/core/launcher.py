from __future__ import annotations

from pathlib import Path

from .factory import AgentFactory
from .memory import ConvoGraph


def main() -> None:
    graph = ConvoGraph(Path("convo_graph.json"))
    agent = AgentFactory.create("echo", "echo-agent")
    result = agent.run("Hello")
    graph.append({"agent": agent.name, "task": "Hello", "result": result})
    print(result)


if __name__ == "__main__":
    main()

