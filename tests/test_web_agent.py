import functools
import http.server
import socketserver
import threading
from pathlib import Path

from zlamida_core.core.factory import AgentFactory


def test_web_agent(tmp_path: Path) -> None:
    page = tmp_path / "index.txt"
    page.write_text("hello web")

    class Handler(http.server.SimpleHTTPRequestHandler):
        last_agent = ""

        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(tmp_path), **kwargs)

        def do_GET(self) -> None:  # type: ignore[override]
            Handler.last_agent = self.headers.get("User-Agent", "")
            super().do_GET()

    Handler.protocol_version = "HTTP/1.0"

    with socketserver.TCPServer(("localhost", 0), Handler) as server:
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        try:
            agent = AgentFactory.create("web", "w", memory_path=tmp_path / "g.json")
            result = agent.run(f"http://localhost:{port}/index.txt")
            assert "hello web" in result
            assert Handler.last_agent == agent.USER_AGENT
        finally:
            server.shutdown()
            thread.join()
