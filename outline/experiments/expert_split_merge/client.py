"""Minimal Anthropic-Messages-API client over the configured proxy."""
from __future__ import annotations
import json
import os
import time
import urllib.request
import urllib.error
import http.client
from dataclasses import dataclass


@dataclass
class Reply:
    text: str
    input_tokens: int
    output_tokens: int
    latency_s: float


class Client:
    def __init__(
        self,
        model: str = "claude-haiku-4-5",
        base_url: str | None = None,
        api_key: str | None = None,
        max_tokens: int = 512,
        timeout: int = 120,
    ):
        self.model = model
        self.base_url = base_url or os.environ["ANTHROPIC_BASE_URL"]
        self.api_key = api_key or os.environ["ANTHROPIC_AUTH_TOKEN"]
        self.max_tokens = max_tokens
        self.timeout = timeout

    def call(
        self,
        system: str,
        user: str,
        max_tokens: int | None = None,
        retries: int = 5,
    ) -> Reply:
        body = {
            "model": self.model,
            "max_tokens": max_tokens or self.max_tokens,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        }
        url = f"{self.base_url.rstrip('/')}/v1/messages"
        data = json.dumps(body).encode()
        last_err: Exception | None = None
        for attempt in range(retries + 1):
            req = urllib.request.Request(
                url,
                data=data,
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                method="POST",
            )
            t0 = time.time()
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    payload = json.loads(resp.read())
                latency = time.time() - t0
                txt_parts = [b["text"] for b in payload.get("content", []) if b.get("type") == "text"]
                txt = "".join(txt_parts)
                u = payload.get("usage", {})
                return Reply(
                    text=txt,
                    input_tokens=u.get("input_tokens", 0),
                    output_tokens=u.get("output_tokens", 0),
                    latency_s=latency,
                )
            except (
                urllib.error.URLError,
                urllib.error.HTTPError,
                TimeoutError,
                http.client.RemoteDisconnected,
                http.client.IncompleteRead,
                http.client.HTTPException,
                ConnectionResetError,
                OSError,
            ) as e:
                last_err = e
                # exponential backoff capped at 8s
                time.sleep(min(8.0, 1.5 * (2 ** attempt)))
                continue
        raise RuntimeError(f"client failed after retries: {last_err!r}")


if __name__ == "__main__":
    c = Client()
    r = c.call("You are terse.", "Reply with the single word OK.")
    print(repr(r))
