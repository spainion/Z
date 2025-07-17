from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Tuple

import uvicorn

from .core.factory import AgentFactory
from .core.memory import ConvoGraph
from .core import process_runner, runner


def run_agent(agent_type: str, name: str, task: str) -> None:
    graph = ConvoGraph(Path("convo_graph.json"))
    agent = AgentFactory.create(agent_type, name)
    result = agent.run(task)
    graph.append({"agent": name, "task": task, "result": result})
    print(result)


def run_batch(tasks: Iterable[Tuple[str, str, str]], use_process: bool = False) -> None:
    """Run multiple agents concurrently and log results."""
    graph = ConvoGraph(Path("convo_graph.json"))
    run_fn = process_runner.run_agents if use_process else runner.run_agents
    results = run_fn(tasks)
    for (agent_type, name, task) in tasks:
        graph.append({"agent": name, "task": task, "result": results[name]})
        print(f"{name}: {results[name]}")


def main() -> None:
    parser = argparse.ArgumentParser(description="ZΛMIDΛ_CORE CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run-agent", help="Run a single agent once")
    run_p.add_argument("agent_type", help="Registered agent type")
    run_p.add_argument("name", help="Agent instance name")
    run_p.add_argument("task", help="Task text")

    batch_p = sub.add_parser("run-batch", help="Run multiple agents")
    batch_p.add_argument(
        "--task",
        dest="tasks",
        action="append",
        required=True,
        help="Comma-separated agent_type,name,task specification",
    )
    batch_p.add_argument(
        "--process",
        action="store_true",
        help="Use process-based runner",
    )

    serve_p = sub.add_parser("serve", help="Launch HTTP API server")
    serve_p.add_argument("--host", default="127.0.0.1")
    serve_p.add_argument("--port", type=int, default=8000)

    args = parser.parse_args()

    if args.cmd == "run-agent":
        run_agent(args.agent_type, args.name, args.task)
    elif args.cmd == "run-batch":
        task_specs = [tuple(t.split(',', 2)) for t in args.tasks]
        run_batch(task_specs, use_process=args.process)
    elif args.cmd == "serve":
        uvicorn.run("zlamida_core.ui.server:app", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
