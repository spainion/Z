import asyncio
import os
from zlamida_core.agents.async_openai_agent import AsyncOpenAIAgent


class DummyResult:
    def __init__(self, text: str) -> None:
        self.choices = [type("Choice", (), {"message": type("Msg", (), {"content": text})()})()]


def test_async_openai_agent(monkeypatch, tmp_path):
    called = {}

    async def fake_create(*args, **kwargs):
        called["done"] = True
        return DummyResult("yo")

    class DummyClient:
        class Chat:
            class Completions:
                create = staticmethod(fake_create)

            completions = Completions()

        chat = Chat()

    monkeypatch.setattr("openai.AsyncOpenAI", lambda api_key=None: DummyClient())
    monkeypatch.setenv("OPENAI_API_KEY", "x")
    agent = AsyncOpenAIAgent("a", memory_path=tmp_path / "g.json")
    result = asyncio.run(agent.arun("hi"))
    assert result == "yo"
    assert called["done"]


