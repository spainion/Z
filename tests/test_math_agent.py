from zlamida_core.core.factory import AgentFactory


def test_math_agent(tmp_path):
    agent = AgentFactory.create("math", "calc", memory_path=tmp_path / "g.json")
    assert agent.run("2+3*4") == 14
