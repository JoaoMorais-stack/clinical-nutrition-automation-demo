from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from clinical_demo.adapters import SyntheticCaseAdapter
from clinical_demo.repository import SQLiteRunRepository
from clinical_demo.service import NutritionWorkflowService


PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATIC_ROOT = PROJECT_ROOT / "static"


class DemoRequestHandler(BaseHTTPRequestHandler):
    service: NutritionWorkflowService

    def _send_bytes(self, content: bytes, content_type: str, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def _send_json(self, payload: Any, status: int = 200) -> None:
        encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self._send_bytes(encoded, "application/json; charset=utf-8", status)

    def _read_json(self) -> dict[str, Any]:
        length = min(int(self.headers.get("Content-Length", "0")), 16_384)
        if not length:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def do_GET(self) -> None:
        if self.path == "/api/dashboard":
            self._send_json(self.service.dashboard())
            return

        static_files = {
            "/": ("index.html", "text/html; charset=utf-8"),
            "/styles.css": ("styles.css", "text/css; charset=utf-8"),
            "/app.js": ("app.js", "text/javascript; charset=utf-8"),
        }
        selected = static_files.get(self.path)
        if selected is None:
            self._send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)
            return
        filename, content_type = selected
        self._send_bytes((STATIC_ROOT / filename).read_bytes(), content_type)

    def do_POST(self) -> None:
        try:
            payload = self._read_json()
            if self.path == "/api/run":
                care_area = str(payload.get("care_area", "")).strip() or None
                self._send_json(self.service.run(care_area))
                return
            if self.path == "/api/reset":
                self._send_json(self.service.reset())
                return
            self._send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)
        except (ValueError, KeyError, json.JSONDecodeError) as error:
            self._send_json({"error": str(error)}, HTTPStatus.BAD_REQUEST)

    def log_message(self, message_format: str, *args: Any) -> None:
        print(f"[local-demo] {message_format % args}")


def build_server(host: str, port: int, database_path: Path) -> ThreadingHTTPServer:
    repository = SQLiteRunRepository(database_path)
    service = NutritionWorkflowService(SyntheticCaseAdapter(), repository)

    class BoundHandler(DemoRequestHandler):
        pass

    BoundHandler.service = service
    return ThreadingHTTPServer((host, port), BoundHandler)


def serve(host: str, port: int, database_path: Path) -> None:
    server = build_server(host, port, database_path)
    print(f"Clinical Nutrition Automation Demo: http://{host}:{port}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDemo stopped.")
    finally:
        server.server_close()

