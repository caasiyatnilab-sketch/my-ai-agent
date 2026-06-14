"""Simple JSONL conversation memory."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .providers import Message


class JsonlMemory:
    """Append-only conversation memory suitable for local CLI usage."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self, limit: int = 20) -> list[Message]:
        if not self.path.exists():
            return []

        # Read only the last 64KB to avoid loading huge files into memory.
        # This is a simple but effective defense against OOM on large history files.
        try:
            with self.path.open("rb") as f:
                f.seek(0, 2)
                file_size = f.tell()
                f.seek(max(0, file_size - 64 * 1024))
                chunk = f.read().decode("utf-8", errors="ignore")
        except OSError:
            return []

        messages: list[Message] = []
        for line in chunk.splitlines()[-limit:]:
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
