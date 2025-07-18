import subprocess
import sys
import os
from pathlib import Path


def test_list_agents_cli(tmp_path):
    env = {**os.environ, "PYTHONPATH": str(Path(__file__).resolve().parents[1])}
    result = subprocess.run(
        [sys.executable, '-m', 'zlamida_core', 'list-agents'],
        capture_output=True,
        text=True,
        cwd=tmp_path,
        env=env,
    )
    out = result.stdout.strip().splitlines()
    assert 'echo' in out and 'shell' in out


def test_get_context_cli(tmp_path):
    env = {**os.environ, "PYTHONPATH": str(Path(__file__).resolve().parents[1])}
    graph = tmp_path / "g.json"
    subprocess.run(
        [sys.executable, '-m', 'zlamida_core', '--memory', str(graph), 'run-agent', 'echo', 'a', 'hi'],
        check=True,
        env=env,
        text=True,
    )
    result = subprocess.run(
        [sys.executable, '-m', 'zlamida_core', '--memory', str(graph), 'get-context', '--limit', '1'],
        capture_output=True,
        text=True,
        env=env,
    )
    assert 'hi' in result.stdout
