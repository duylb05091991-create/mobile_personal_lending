"""Run the one-process HTTP simulation with ``python3 -m nopbai``."""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import create_application


APPLICATION = create_application()


class RequestHandler(BaseHTTPRequestHandler):
    def _send(self, status, body):
        payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length) if length else b"{}"
            body = json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
            body = {}
        status, response = APPLICATION.handle("POST", self.path, body, dict(self.headers.items()))
        self._send(status, response)

    def do_GET(self):
        status, response = APPLICATION.handle("GET", self.path, {}, dict(self.headers.items()))
        self._send(status, response)

    def log_message(self, format_string, *args):
        return


def main():
    host = os.environ.get("NOPBAI_HOST", "127.0.0.1")
    port = int(os.environ.get("NOPBAI_PORT", "8080"))
    server = ThreadingHTTPServer((host, port), RequestHandler)
    print("Nopbai Personal Loan runtime listening on http://{0}:{1}".format(host, port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

