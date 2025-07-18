from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Tuple

import uvicorn

from .core.factory import AgentFactory
from .core.memory import ConvoGraph
from .core import process_runner, runner
from .core.log import get_logger


def run_agent(agent_type: str, name: str, task: str, memory_path: Path) -> None:
    logger = get_logger(__name__)
    graph = ConvoGraph(memory_path)
    agent = AgentFactory.create(agent_type, name, memory_path=graph.path)
    result = agent.run(task)
    graph.append({"agent": name, "task": task, "result": result})
    logger.info("%s -> %s", name, result)
    print(result)


def run_batch(
    tasks: Iterable[Tuple[str, str, str]],
    memory_path: Path,
    use_process: bool = False,
    max_workers: int | None = None,
) -> None:
    """Run multiple agents concurrently and log results.

    Args:
        tasks: Iterable of (agent_type, name, task) tuples.
        memory_path: JSON file path for storing results.
        use_process: Whether to use processes instead of threads.
        max_workers: Limit the number of concurrent workers.
    """
    logger = get_logger(__name__)
    graph = ConvoGraph(memory_path)
    run_fn = process_runner.run_agents if use_process else runner.run_agents
    results = run_fn([(a, n, t) for a, n, t in tasks], max_workers=max_workers)
    for agent_type, name, task in tasks:
        graph.append({"agent": name, "task": task, "result": results[name]})
        logger.info("%s -> %s", name, results[name])
        print(f"{name}: {results[name]}")


def main() -> None:
    parser = argparse.ArgumentParser(description="ZΛMIDΛ_CORE CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)
    parser.add_argument(
        "--memory",
        default="convo_graph.json",
        help="Path to memory JSON file",
    )

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
    batch_p.add_argument(
        "--max-workers",
        type=int,
        default=None,
        help="Maximum number of concurrent workers",
    )

    serve_p = sub.add_parser("serve", help="Launch HTTP API server")
    serve_p.add_argument("--host", default="127.0.0.1")
    serve_p.add_argument("--port", type=int, default=8000)

    args = parser.parse_args()

    if args.cmd == "run-agent":
        run_agent(args.agent_type, args.name, args.task, Path(args.memory))
    elif args.cmd == "run-batch":
        task_specs = [tuple(t.split(',', 2)) for t in args.tasks]
        run_batch(
            task_specs,
            Path(args.memory),
            use_process=args.process,
            max_workers=args.max_workers,
        )
    elif args.cmd == "serve":
        uvicorn.run(
            "zlamida_core.ui.server:app",
            host=args.host,
            port=args.port,
            reload=False,
        )


if __name__ == "__main__":
    main()
