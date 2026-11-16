import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from name import generate_greeting


PAGE = Path(__file__).with_name("index.html")
HOST = "127.0.0.1"
PORT = 8000


class GreetingHandler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, data: dict[str, str]) -> None:
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path != "/":
            self.send_error(404)
            return

        body = PAGE.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        if self.path != "/greeting":
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send_json(400, {"error": "Invalid request."})
            return
        if length < 1 or length > 16_384:
            self._send_json(400, {"error": "Request body must be between 1 and 16384 bytes."})
            return

        try:
            payload = json.loads(self.rfile.read(length))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._send_json(400, {"error": "Request body must be valid JSON."})
            return

        if not isinstance(payload, dict) or not isinstance(payload.get("name"), str):
            self._send_json(400, {"error": "Please provide a name."})
            return

        name = payload["name"].strip()
        if not name or len(name) > 120:
            self._send_json(400, {"error": "Name must be between 1 and 120 characters."})
            return

        try:
            greeting = generate_greeting(name)
        except RuntimeError as error:
            self.log_error("Greeting generation failed: %s", error)
            self._send_json(502, {"error": str(error)})
            return

        self._send_json(200, {"greeting": greeting})


if __name__ == "__main__":
    print(f"Open http://{HOST}:{PORT} in your browser.")
    ThreadingHTTPServer((HOST, PORT), GreetingHandler).serve_forever()
