from zlamida_core.core.runner import run_agents
from zlamida_core.core.factory import AgentFactory


def test_run_agents():
    tasks = [
        ("echo", "a", "one"),
        ("echo", "b", "two"),
    ]
    results = run_agents(tasks)
    assert results == {"a": "one", "b": "two"}

from zlamida_core.core import process_runner


def test_process_runner():
    tasks = [
        ("shell", "sh1", "echo hi"),
        ("shell", "sh2", "echo there"),
    ]
    results = process_runner.run_agents(tasks)
    assert results == {"sh1": "hi", "sh2": "there"}
