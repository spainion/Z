from pathlib import Path
import os

from zlamida_core.core.memory import ConvoGraph


def test_memory(tmp_path: Path):
    path = tmp_path / "graph.json"
    graph = ConvoGraph(path)
    graph.append({"msg": "hi"})
    assert graph.all() == [{"msg": "hi"}]
    assert path.exists()


def test_memory_creates_dirs(tmp_path: Path):
    sub = tmp_path / "sub" / "graph.json"
    graph = ConvoGraph(sub)
    graph.append({"msg": "hi"})
    assert sub.exists()
