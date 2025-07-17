from __future__ import annotations

import argparse
from pathlib import Path

import uvicorn

from .core.factory import AgentFactory
from .core.memory import ConvoGraph


def run_agent(agent_type: str, name: str, task: str) -> None:
    graph = ConvoGraph(Path("convo_graph.json"))
    agent = AgentFactory.create(agent_type, name)
    result = agent.run(task)
    graph.append({"agent": name, "task": task, "result": result})
    print(result)


def main() -> None:
    parser = argparse.ArgumentParser(description="ZΛMIDΛ_CORE CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run-agent", help="Run a single agent once")
    run_p.add_argument("agent_type", help="Registered agent type")
    run_p.add_argument("name", help="Agent instance name")
    run_p.add_argument("task", help="Task text")

    serve_p = sub.add_parser("serve", help="Launch HTTP API server")
    serve_p.add_argument("--host", default="127.0.0.1")
    serve_p.add_argument("--port", type=int, default=8000)

    args = parser.parse_args()

    if args.cmd == "run-agent":
        run_agent(args.agent_type, args.name, args.task)
    elif args.cmd == "serve":
        uvicorn.run("zlamida_core.ui.server:app", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
