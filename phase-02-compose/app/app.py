"""Dojo app: proves container -> emulator connectivity.

GET /health -> {"status": "ok"}
GET /s3     -> {"buckets": [...]} via AWS_ENDPOINT_URL (service-name DNS in compose).
"""
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

import boto3

ENDPOINT = os.environ.get("AWS_ENDPOINT_URL", "http://localhost:4566")
REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")


def s3_buckets():
    s3 = boto3.client("s3", endpoint_url=ENDPOINT, region_name=REGION)
    return [b["Name"] for b in s3.list_buckets().get("Buckets", [])]


class Handler(BaseHTTPRequestHandler):
    def _send(self, payload, code=200):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._send({"status": "ok"})
        elif self.path == "/s3":
            try:
                self._send({"buckets": s3_buckets(), "endpoint": ENDPOINT})
            except Exception as e:  # noqa: BLE001 - surface emulator errors plainly
                self._send({"error": str(e), "endpoint": ENDPOINT}, code=502)
        else:
            self._send({"error": "not found"}, code=404)

    def log_message(self, *args):  # keep logs clean
        pass


if __name__ == "__main__":
    print(f"dojo-app serving on :8080, emulator at {ENDPOINT}", flush=True)
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
