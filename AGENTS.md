# Project Contribution Guidelines

This repository provides a modular multi-agent framework. To ensure agents built elsewhere can sync and interoperate with this system:

## Environment Setup
1. Install dependencies with `pip install -r requirements.txt`.
2. Run the test suite via `PYTHONPATH=. pytest -q` before committing changes.

## Adding Agents
- Place agent modules under `zlamida_core/agents/` and register them in `AgentFactory`.
- Agents should persist results to `ConvoGraph` so others can learn from prior runs.
- Logging is configured via `zlamida_core.core.log`. Use `log.get_logger(__name__)` in new modules.

## Syncing with External Systems
- External agents may read and append to `convo_graph.json` for shared memory.
- Keep logs in `zlamida.log` for debugging and auditability.
- Avoid monkeypatching; use real API calls and subprocesses where needed.
