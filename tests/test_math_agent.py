from zlamida_core.core.factory import AgentFactory


def test_math_agent(tmp_path):
    agent = AgentFactory.create("math", "calc", memory_path=tmp_path / "g.json")
    assert agent.run("2+3*4") == 14
    assert agent.run("(1+2)*3") == 9
    assert agent.run("-5 + 10/2") == 0
