from zlamida_core.core.factory import AgentFactory


def test_echo_agent():
    agent = AgentFactory.create("echo", "tester")
    assert agent.run("hi") == "hi"


def test_openai_agent(monkeypatch):
    class FakeResp:
        choices = [type("Obj", (), {"message": {"content": "response"}})]

    def fake_create(*args, **kwargs):
        return FakeResp()

    monkeypatch.setenv("OPENAI_API_KEY", "x")
    from zlamida_core.agents import openai_agent

    monkeypatch.setattr(openai_agent.openai.ChatCompletion, "create", fake_create)

    agent = AgentFactory.create("openai", "tester")
    assert agent.run("hi") == "response"


def test_shell_agent(tmp_path):
    agent = AgentFactory.create("shell", "sh")
    result = agent.run("echo hello")
    assert result.strip() == "hello"
