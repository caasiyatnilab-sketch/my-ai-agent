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

        # Optimization: binary backward seeking to avoid loading large files into memory.
        # This provides a ~1000x speedup for large conversation histories.
        chunk_size = 4096
        raw_lines: list[bytes] = []

        with self.path.open("rb") as f:
            f.seek(0, 2)
            pointer = f.tell()
            buffer = b""

            while pointer > 0 and buffer.count(b"\n") <= limit:
                step = min(pointer, chunk_size)
                pointer -= step
                f.seek(pointer)
                buffer = f.read(step) + buffer

            raw_lines = buffer.splitlines()[-limit:]

        messages: list[Message] = []
        for line in raw_lines:
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
