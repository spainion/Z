from zlamida_core.core.factory import AgentFactory
import os
import pytest


def test_echo_agent(tmp_path):
    agent = AgentFactory.create("echo", "tester", memory_path=tmp_path/"g.json")
    assert agent.run("hi") == "hi"


@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set"
)
def test_openai_agent_real(tmp_path):
    """Run OpenAI agent against the real API if a key is configured."""
    agent = AgentFactory.create("openai", "tester", memory_path=tmp_path/"g.json")
    result = agent.run("hi")
    assert isinstance(result, str) and len(result) > 0


def test_shell_agent(tmp_path):
    agent = AgentFactory.create("shell", "sh", memory_path=tmp_path/"g.json")
    result = agent.run("echo hello")
    assert result.strip() == "hello"
