"""Simple JSONL conversation memory."""

from __future__ import annotations

import json
import os
from dataclasses import asdict
from pathlib import Path

from .providers import Message


class JsonlMemory:
    """Append-only conversation memory suitable for local CLI usage."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self, limit: int = 20) -> list[Message]:
        """Load the last N messages from the JSONL file without reading the whole file."""
        if not self.path.exists():
            return []

        file_size = self.path.stat().st_size
        if file_size == 0:
            return []

        messages: list[Message] = []
        buffer_size = 4096

        with self.path.open("rb") as f:
            f.seek(0, os.SEEK_END)
            pos = f.tell()
            leftover = b""

            while pos > 0 and len(messages) < limit:
                read_size = min(pos, buffer_size)
                pos -= read_size
                f.seek(pos)
                chunk = f.read(read_size) + leftover

                lines = chunk.splitlines()
                # The first line of the chunk might be incomplete (unless pos is 0)
                if pos > 0:
                    leftover = lines[0]
                    lines = lines[1:]
                else:
                    leftover = b""

                for line in reversed(lines):
                    if not line.strip():
                        continue
                    try:
                        data = json.loads(line.decode("utf-8"))
                        messages.append(
                            Message(role=str(data["role"]), content=str(data["content"]))
                        )
                        if len(messages) >= limit:
                            break
                    except (json.JSONDecodeError, KeyError, UnicodeDecodeError):
                        continue

        messages.reverse()
        return messages

    def append(self, message: Message) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(asdict(message), ensure_ascii=False) + "\n")
