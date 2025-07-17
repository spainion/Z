from zlamida_core.core.runner import run_agents
from zlamida_core.core.factory import AgentFactory


def test_run_agents():
    tasks = [
        ("echo", "a", "one"),
        ("echo", "b", "two"),
    ]
    results = run_agents(tasks)
    assert results == {"a": "one", "b": "two"}
