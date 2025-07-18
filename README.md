# ZΛMIDΛ_CORE

A minimal implementation of a modular multi-agent system. This repository provides a simple
foundation with an agent factory, persistent memory graph, and a FastAPI-based UI.
Current version: 0.2.6.

## Features

- **Agents**: Base class with `EchoAgent`, API-backed `OpenAIAgent`, `ShellAgent` for shell commands, and `OrchestratorAgent` for chaining agents.
- **AgentFactory**: Dynamically registers and creates agent instances.
- **Memory**: `ConvoGraph` stores interactions in an append-only JSON file.
  Recent interactions can be queried via `ConvoGraph.context()` for any agent.
- **UI**: Basic FastAPI server to run agents and inspect history.
- **Logging**: All actions are recorded to `zlamida.log` and every agent
  persists its results to `convo_graph.json` by default. Use `--memory` or the
  `MEMORY_PATH` environment variable to specify a custom location. Set
  `LOG_FILE` to change the log destination.

Run `python -m zlamida_core run-agent echo demo "hi"` to execute a single agent or `python -m zlamida_core serve` to start the API. Use `--memory path/to/file.json` to customize the memory file or set the `MEMORY_PATH` environment variable which the CLI and server both honour. To use the `OpenAIAgent`, set the `OPENAI_API_KEY` environment variable.
Use `python -m zlamida_core run-batch --task echo,a,hi --task shell,b,"echo there" --memory mygraph.json` to run agents concurrently. Pass `--process` to isolate agents in separate processes.
`OrchestratorAgent` can chain tasks: `python -c "from zlamida_core.agents.orchestrator_agent import OrchestratorAgent; print(OrchestratorAgent('orch').run([('echo','a','hi'),('shell','b','echo there')]))"`.

- **Runner**: `run_agents` executes agents in threads, and `process_runner.run_agents` does so in separate processes.
- **Listing**: `python -m zlamida_core list-agents` shows all available agent types.
- **Context**: `python -m zlamida_core get-context --limit 5` prints recent history.

## Development

Install dependencies and run tests:

```bash
pip install -r requirements.txt
PYTHONPATH=. pytest -q
```

Tests exercising `OpenAIAgent` use the OpenAI Python client `>=1.0`.
Provide an `OPENAI_API_KEY` to run them against the live API or they will
be skipped. Execution logs are stored in `zlamida.log` by default. Set
`LOG_FILE` to change the path.

See `CHANGELOG.md` for release notes.
