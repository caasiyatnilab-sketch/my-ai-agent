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
        """Load the last `limit` messages from the JSONL history."""
        if not self.path.exists():
            return []

        lines: list[bytes] = []
        chunk_size = 4096

        # Efficiently read the last N lines by seeking to the end and reading backwards.
        with self.path.open("rb") as f:
            f.seek(0, 2)
            pointer = f.tell()
            buffer = b""

            while pointer > 0 and len(lines) <= limit:
                step = min(pointer, chunk_size)
                pointer -= step
                f.seek(pointer)
                chunk = f.read(step)
                buffer = chunk + buffer
                lines = buffer.splitlines()

        messages: list[Message] = []
        # If we didn't reach the start of the file, the first line in our buffer
        # might be incomplete, so we only take the last `limit` lines.
        for line in lines[-limit:]:
            if not line.strip():
                continue
            try:
                data = json.loads(line.decode("utf-8"))
                messages.append(Message(role=str(data["role"]), content=str(data["content"])))
            except (json.JSONDecodeError, KeyError, UnicodeDecodeError):
                continue
        return messages

    def append(self, message: Message) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(asdict(message), ensure_ascii=False) + "\n")
