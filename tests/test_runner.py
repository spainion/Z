from zlamida_core.core.runner import run_agents
from zlamida_core import __main__
import json
from pathlib import Path


def test_run_agents():
    tasks = [
        ("echo", "a", "one"),
        ("echo", "b", "two"),
    ]
    results = run_agents(tasks)
    assert results == {"a": "one", "b": "two"}

    limited = run_agents(tasks, max_workers=1)
    assert limited == {"a": "one", "b": "two"}

from zlamida_core.core import process_runner


def test_process_runner():
    tasks = [
        ("shell", "sh1", "echo hi"),
        ("shell", "sh2", "echo there"),
    ]
    results = process_runner.run_agents(tasks)
    assert results == {"sh1": "hi", "sh2": "there"}

    limited = process_runner.run_agents(tasks, max_workers=1)
    assert limited == {"sh1": "hi", "sh2": "there"}


def test_run_batch(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    tasks = [
        ("echo", "a", "hi"),
        ("echo", "b", "bye"),
    ]
    __main__.run_batch(tasks, Path("convo_graph.json"), max_workers=1)
    data = json.loads(Path("convo_graph.json").read_text())
    assert any(entry["result"] == "hi" for entry in data)
    assert Path(__file__).resolve().parents[1].joinpath("zlamida.log").exists()

