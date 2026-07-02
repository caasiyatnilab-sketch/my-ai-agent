"""Simple JSONL conversation memory."""

from __future__ import annotations

import json
import os
from pathlib import Path

from .providers import Message


class JsonlMemory:
    """Append-only conversation memory suitable for local CLI usage."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self, limit: int = 20) -> list[Message]:
        """Load the last N messages from memory using backward seeking for performance."""
        if not self.path.exists():
            return []

        chunk_size = 4096
        messages: list[Message] = []

        with self.path.open("rb") as f:
            f.seek(0, os.SEEK_END)
            pointer = f.tell()
            buffer = b""

            while pointer > 0 and buffer.count(b"\n") <= limit:
                step = min(pointer, chunk_size)
                pointer -= step
                f.seek(pointer)
                buffer = f.read(step) + buffer

            lines = buffer.split(b"\n")
            # JSONL files often end with a newline, resulting in an empty last element.
            if lines and not lines[-1]:
                lines.pop()

            for line_bytes in lines[-limit:]:
                try:
                    data = json.loads(line_bytes.decode("utf-8"))
                    messages.append(Message(role=str(data["role"]), content=str(data["content"])))
                except (json.JSONDecodeError, KeyError, UnicodeDecodeError):
                    continue

        return messages

    def append(self, message: Message) -> None:
        """Append a message to the memory file."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            # Optimized: message.__dict__ is significantly faster than asdict(message)
            # for simple dataclasses as it avoids recursive inspection and copying.
            stream.write(json.dumps(message.__dict__, ensure_ascii=False) + "\n")
