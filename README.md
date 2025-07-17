# ZΛMIDΛ_CORE

A minimal implementation of a modular multi-agent system. This repository provides a simple
foundation with an agent factory, persistent memory graph, and a FastAPI-based UI.

## Features

- **Agents**: Base class with `EchoAgent` and API-backed `OpenAIAgent`.
- **AgentFactory**: Dynamically registers and creates agent instances.
- **Memory**: `ConvoGraph` stores interactions in an append-only JSON file.
- **UI**: Basic FastAPI server to run agents and inspect history.

Run `python -m zlamida_core run-agent echo demo "hi"` to execute a sample agent or `python -m zlamida_core serve` to start the API. To use the `OpenAIAgent`, set the `OPENAI_API_KEY` environment variable.

- **Runner**: `run_agents` executes multiple agents concurrently using a thread pool.

## Development

Install dependencies and run tests:

```bash
pip install -r requirements.txt
PYTHONPATH=. pytest -q
```
