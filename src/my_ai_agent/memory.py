"""Simple JSONL conversation memory."""

from __future__ import annotations

from dataclasses import asdict
import json
import os
from pathlib import Path

from .providers import Message


class JsonlMemory:
    """Append-only conversation memory suitable for local CLI usage."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self, limit: int = 20) -> list[Message]:
        if not self.path.exists():
            return []

        # Memory efficient tail read: read from the end of the file in chunks.
        messages: list[Message] = []
        chunk_size = 4096
        with self.path.open("rb") as f:
            f.seek(0, os.SEEK_END)
            file_size = f.tell()
            buffer = b""
            pos = file_size
            lines_found = 0

            while pos > 0 and lines_found <= limit:
                read_size = min(pos, chunk_size)
                pos -= read_size
                f.seek(pos, os.SEEK_SET)
                chunk = f.read(read_size)
                buffer = chunk + buffer
                lines_found = buffer.count(b"\n")

            lines = buffer.splitlines()
            # If the file doesn't end with a newline, buffer.splitlines() handles it correctly.
            # We want the last 'limit' messages.
            for line in lines[-limit:]:
                if not line:
                    continue
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
