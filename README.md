# ZΛMIDΛ_CORE

A minimal implementation of a modular multi-agent system. This repository provides a simple
foundation with an agent factory, persistent memory graph, and a FastAPI-based UI.

## Features

- **Agents**: Base class with `EchoAgent`, API-backed `OpenAIAgent`, and `ShellAgent` for running shell commands.
- **AgentFactory**: Dynamically registers and creates agent instances.
- **Memory**: `ConvoGraph` stores interactions in an append-only JSON file.
- **UI**: Basic FastAPI server to run agents and inspect history.

Run `python -m zlamida_core run-agent echo demo "hi"` to execute a single agent or `python -m zlamida_core serve` to start the API. To use the `OpenAIAgent`, set the `OPENAI_API_KEY` environment variable.
Use `python -m zlamida_core run-batch --task echo,a,hi --task shell,b,"echo there"` to run agents concurrently. Pass `--process` to isolate agents in separate processes.

- **Runner**: `run_agents` executes agents in threads, and `process_runner.run_agents` does so in separate processes.

## Development

Install dependencies and run tests:

```bash
pip install -r requirements.txt
PYTHONPATH=. pytest -q
```

Tests exercising `OpenAIAgent` use the OpenAI Python client `>=1.0`.
Provide an `OPENAI_API_KEY` to run them against the live API or they will
be skipped.
