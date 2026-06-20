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

        # Seek to the end and read backwards to find the last `limit` lines.
        # This is O(limit) instead of O(file_size).
        lines: list[bytes] = []
        try:
            with self.path.open("rb") as f:
                f.seek(0, 2)  # Seek to end
                file_size = f.tell()
                pointer = file_size
                buffer = b""
                chunk_size = 4096

                while pointer > 0 and len(lines) <= limit:
                    pointer = max(0, pointer - chunk_size)
                    f.seek(pointer)
                    chunk = f.read(min(chunk_size, file_size - pointer))
                    buffer = chunk + buffer

                    while b"\n" in buffer:
                        idx = buffer.rfind(b"\n")
                        line = buffer[idx + 1 :]
                        if line:
                            lines.append(line)
                        buffer = buffer[:idx]
                        if len(lines) >= limit:
                            break

                if len(lines) < limit and buffer:
                    lines.append(buffer)
        except OSError:
            return []

        messages: list[Message] = []
        for raw_line in lines[:limit][::-1]:
            try:
                line = raw_line.decode("utf-8")
                data = json.loads(line)
                messages.append(Message(role=str(data["role"]), content=str(data["content"])))
            except (json.JSONDecodeError, KeyError):
                continue
        return messages

    def append(self, message: Message) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(asdict(message), ensure_ascii=False) + "\n")
