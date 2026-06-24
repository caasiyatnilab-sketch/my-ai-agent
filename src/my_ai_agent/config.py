"""Configuration helpers for the agent."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AgentConfig:
    """Runtime settings for the agent.

    The default provider is ``mock`` so the CLI and tests work without network access or API keys.
    Set ``MY_AI_AGENT_PROVIDER=openai`` and ``OPENAI_API_KEY`` to use an OpenAI-compatible endpoint.
    """

    provider: str = "mock"
    model: str = "gpt-4.1-mini"
    system_prompt: str = (
        "You are a careful, practical AI agent. Be concise and verify tool results."
    )
    temperature: float = 0.2
    timeout_seconds: float = 30.0
    max_retries: int = 2
    memory_path: Path = Path(".agent-memory.jsonl")
    workspace: Path = Path.cwd()
    openai_base_url: str = "https://api.openai.com/v1"
    openai_api_key: str | None = None

    @classmethod
    def from_env(cls) -> AgentConfig:
        """Build configuration from environment variables."""

        return cls(
            provider=os.getenv("MY_AI_AGENT_PROVIDER", "mock").strip().lower(),
            model=os.getenv("MY_AI_AGENT_MODEL", "gpt-4.1-mini"),
            system_prompt=os.getenv(
                "MY_AI_AGENT_SYSTEM_PROMPT",
                "You are a careful, practical AI agent. Be concise and verify tool results.",
            ),
            temperature=float(os.getenv("MY_AI_AGENT_TEMPERATURE", "0.2")),
            timeout_seconds=float(os.getenv("MY_AI_AGENT_TIMEOUT", "30")),
            max_retries=int(os.getenv("MY_AI_AGENT_MAX_RETRIES", "2")),
            memory_path=Path(os.getenv("MY_AI_AGENT_MEMORY", ".agent-memory.jsonl")),
            workspace=Path(os.getenv("MY_AI_AGENT_WORKSPACE", str(Path.cwd()))).resolve(),
            openai_base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
        )
