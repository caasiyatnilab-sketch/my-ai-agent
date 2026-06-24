"""Language model provider implementations."""

from __future__ import annotations

from dataclasses import dataclass
import json
import time
from typing import Protocol
from urllib import error, request

from .config import AgentConfig


@dataclass(frozen=True)
class Message:
    role: str
    content: str


class Provider(Protocol):
    """Protocol implemented by all text generation providers."""

    def complete(self, messages: list[Message]) -> str:
        """Return assistant text for the provided chat messages."""


class MockProvider:
    """Deterministic provider that makes the project usable offline."""

    def complete(self, messages: list[Message]) -> str:
        user_messages = [message.content for message in messages if message.role == "user"]
        latest = user_messages[-1] if user_messages else ""
        if "tool:" in latest.lower():
            return "I reviewed the tool output and can continue with the next step."
        return (
            f"Mock response: received {len(latest)} characters. "
            "Configure OPENAI_API_KEY for real LLM calls."
        )


class OpenAICompatibleProvider:
    """Minimal OpenAI-compatible Chat Completions provider using the standard library."""

    def __init__(self, config: AgentConfig) -> None:
        if not config.openai_api_key:
            msg = "OPENAI_API_KEY is required when MY_AI_AGENT_PROVIDER=openai"
            raise ValueError(msg)
        self._config = config

    def complete(self, messages: list[Message]) -> str:
        payload = {
            "model": self._config.model,
            "messages": [message.__dict__ for message in messages],
            "temperature": self._config.temperature,
        }
        body = json.dumps(payload).encode("utf-8")
        req = request.Request(
            f"{self._config.openai_base_url}/chat/completions",
            data=body,
            headers={
                "Authorization": f"Bearer {self._config.openai_api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        last_error: Exception | None = None
        for attempt in range(self._config.max_retries + 1):
            try:
                # Security: limit response size to 1MB to prevent OOM
                with request.urlopen(req, timeout=self._config.timeout_seconds) as response:
                    data = json.loads(response.read(1_048_576).decode("utf-8"))
                return str(data["choices"][0]["message"]["content"])
            except (
                error.HTTPError,
                error.URLError,
                TimeoutError,
                KeyError,
                IndexError,
                json.JSONDecodeError,
            ) as exc:
                last_error = exc
                if attempt >= self._config.max_retries:
                    break
                time.sleep(min(2**attempt, 4))
        raise RuntimeError(f"Provider request failed after retries: {last_error}") from last_error


def build_provider(config: AgentConfig) -> Provider:
    """Create a provider from configuration."""

    if config.provider == "mock":
        return MockProvider()
    if config.provider in {"openai", "openai-compatible"}:
        return OpenAICompatibleProvider(config)
    msg = f"Unsupported provider: {config.provider!r}. Expected 'mock' or 'openai'."
    raise ValueError(msg)
