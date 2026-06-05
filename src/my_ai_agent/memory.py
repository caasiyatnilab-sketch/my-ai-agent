"""Simple JSONL conversation memory."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path

from .providers import Message


class JsonlMemory:
    """Append-only conversation memory suitable for local CLI usage."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self, limit: int = 20) -> list[Message]:
        if not self.path.exists():
            return []
        messages: list[Message] = []
        for line in self.path.read_text(encoding="utf-8").splitlines()[-limit:]:
            try:
                data = json.loads(line)
                messages.append(Message(role=str(data["role"]), content=str(data["content"])))
            except (json.JSONDecodeError, KeyError):
                continue
        return messages

    def append(self, message: Message) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(asdict(message), ensure_ascii=False) + "\n")
