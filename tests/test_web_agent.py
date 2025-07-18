import functools
import http.server
import socketserver
import threading
from pathlib import Path

from zlamida_core.core.factory import AgentFactory


def test_web_agent(tmp_path: Path) -> None:
    page = tmp_path / "index.txt"
    page.write_text("hello web")

    Handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=str(tmp_path)
    )
    with socketserver.TCPServer(("localhost", 0), Handler) as server:
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        try:
            agent = AgentFactory.create("web", "w", memory_path=tmp_path / "g.json")
            result = agent.run(f"http://localhost:{port}/index.txt")
            assert "hello web" in result
        finally:
            server.shutdown()
            thread.join()
