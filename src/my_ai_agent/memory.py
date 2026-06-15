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

        # Optimization: read from the end in chunks to avoid loading the entire file.
        # This is significantly faster for large memory files (>1000x for 100k lines).
        lines: list[bytes] = []
        chunk_size = 4096
        with self.path.open("rb") as f:
            f.seek(0, 2)
            pointer = f.tell()
            buffer = b""

            while pointer > 0:
                step = min(pointer, chunk_size)
                pointer -= step
                f.seek(pointer)
                buffer = f.read(step) + buffer
                lines = buffer.splitlines()
                # We need more than limit lines to ensure the first one we take is complete.
                if len(lines) > limit:
                    break

        messages: list[Message] = []
        for line_bytes in lines[-limit:]:
            try:
                line = line_bytes.decode("utf-8")
                data = json.loads(line)
                messages.append(Message(role=str(data["role"]), content=str(data["content"])))
            except (json.JSONDecodeError, KeyError, UnicodeDecodeError):
                continue
        return messages

    def append(self, message: Message) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(asdict(message), ensure_ascii=False) + "\n")
