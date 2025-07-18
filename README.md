# ZΛMIDΛ_CORE

A minimal implementation of a modular multi-agent system. This repository provides a simple
foundation with an agent factory, persistent memory graph, and a FastAPI-based UI.

## Features

- **Agents**: Base class with `EchoAgent`, API-backed `OpenAIAgent`, `ShellAgent` for shell commands, `WebAgent` for fetching URLs, `MathAgent` for evaluating arithmetic, `OrchestratorAgent` for chaining agents, and `ParallelOrchestratorAgent` for concurrent execution.
- **AgentFactory**: Dynamically registers and creates agent instances.
- **Memory**: `ConvoGraph` stores interactions in an append-only JSON file.
- **UI**: Basic FastAPI server to run agents and inspect history.
- **Logging**: All actions are recorded to `zlamida.log` and every agent
  persists its results to `convo_graph.json` by default. Use `--memory` or the
  `MEMORY_PATH` environment variable to specify a custom location.

Run `python -m zlamida_core run-agent echo demo "hi"` to execute a single agent or `python -m zlamida_core serve` to start the API. Use `--memory path/to/file.json` to customize the memory file. To use the `OpenAIAgent`, set the `OPENAI_API_KEY` environment variable. The server also reads `MEMORY_PATH` for its graph location.
Use `python -m zlamida_core run-batch --task echo,a,hi --task shell,b,"echo there" --memory mygraph.json` to run agents concurrently. Pass `--process` to isolate agents in separate processes.
`OrchestratorAgent` can chain tasks: `python -c "from zlamida_core.agents.orchestrator_agent import OrchestratorAgent; print(OrchestratorAgent('orch').run([('echo','a','hi'),('shell','b','echo there')]))"`.
`ParallelOrchestratorAgent` runs tasks concurrently:
`python -c "from zlamida_core.agents.parallel_orchestrator_agent import ParallelOrchestratorAgent; print(ParallelOrchestratorAgent('orch').run([('echo','a','hi'),('echo','b','bye')]))"`.
Run `python -m zlamida_core run-agent web fetch https://example.com` to fetch a web page via `WebAgent`. The agent sends a custom `User-Agent` header and times out after 10 seconds. Customize the header or timeout with the `WEB_AGENT_UA` and `WEB_AGENT_TIMEOUT` environment variables.
Run `python -m zlamida_core run-agent math calc "2+2*3"` to evaluate an arithmetic expression with `MathAgent`.

- **Runner**: `run_agents` executes agents in threads, and `process_runner.run_agents` does so in separate processes.

## Development

Install dependencies and run tests:

```bash
pip install -r requirements.txt
PYTHONPATH=. pytest -q
```

Tests exercising `OpenAIAgent` use the OpenAI Python client `>=1.0`.
Provide an `OPENAI_API_KEY` to run them against the live API or they will
be skipped. Execution logs are stored in `zlamida.log`.
