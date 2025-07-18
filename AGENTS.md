# Project Contribution Guidelines

This repository provides a modular multi-agent framework. To ensure agents built elsewhere can sync and interoperate with this system:

## Environment Setup
1. Install dependencies with `pip install -r requirements.txt`.
2. Run the test suite via `PYTHONPATH=. pytest -q` before committing changes.

## Adding Agents
- Place agent modules under `zlamida_core/agents/` and register them in `AgentFactory`.
- Agents should persist results to `ConvoGraph` so others can learn from prior runs.
- Use `ConvoGraph.context()` to retrieve recent interactions for an agent.
- Agents automatically record results to `convo_graph.json` unless a custom path is provided. The CLI and server honour a `MEMORY_PATH` environment variable so you can skip the `--memory` flag.
- Logging is configured via `zlamida_core.core.log`. Set `LOG_FILE` to control where logs are written and use `log.get_logger(__name__)` in new modules.
- List registered agent types with `python -m zlamida_core list-agents`.
- Retrieve history with `python -m zlamida_core get-context --limit 5`.

## Syncing with External Systems
- External agents may read and append to `convo_graph.json` for shared memory.
- Keep logs in the file specified by `LOG_FILE` (default `zlamida.log`) for debugging and auditability.
- Avoid monkeypatching; use real API calls and subprocesses where needed.
