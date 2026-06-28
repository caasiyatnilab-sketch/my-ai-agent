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
        # Use binary seeking for O(1) memory loading of large history files
        chunk_size = 4096
        with self.path.open("rb") as f:
            f.seek(0, 2)
            file_size = f.tell()
            buffer = b""
            pointer = file_size
            lines_found = 0
            while pointer > 0 and lines_found <= limit:
                step = min(pointer, chunk_size)
                pointer -= step
                f.seek(pointer)
                chunk = f.read(step)
                buffer = chunk + buffer
                lines_found = buffer.count(b"\n")

            raw_lines = buffer.splitlines()[-limit:]
            for line in raw_lines:
                try:
                    data = json.loads(line.decode("utf-8"))
                    messages.append(Message(role=str(data["role"]), content=str(data["content"])))
                except (json.JSONDecodeError, KeyError):
                    continue
        return messages

    def append(self, message: Message) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(asdict(message), ensure_ascii=False) + "\n")
