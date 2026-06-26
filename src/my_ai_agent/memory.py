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

        # Efficiently read the last `limit` lines using binary backward seeking
        lines: list[bytes] = []
        chunk_size = 4096
        with self.path.open("rb") as f:
            f.seek(0, 2)
            pointer = f.tell()
            buffer = b""
            while pointer > 0 and len(lines) <= limit:
                step = min(pointer, chunk_size)
                pointer -= step
                f.seek(pointer)
                chunk = f.read(step) + buffer
                parts = chunk.split(b"\n")
                if len(parts) > 1:
                    lines.extend(reversed(parts[1:]))
                    buffer = parts[0]
                else:
                    buffer = chunk
            if buffer:
                lines.append(buffer)

        messages: list[Message] = []
        # Filter empty lines and process the last `limit` messages in chronological order
        valid_lines = [line for line in lines if line.strip()]
        for line_bytes in reversed(valid_lines[:limit]):
            try:
                data = json.loads(line_bytes.decode("utf-8"))
                messages.append(Message(role=str(data["role"]), content=str(data["content"])))
            except (json.JSONDecodeError, KeyError):
                continue
        return messages

    def append(self, message: Message) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(asdict(message), ensure_ascii=False) + "\n")
