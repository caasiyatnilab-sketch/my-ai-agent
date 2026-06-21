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
        if not self.path.exists():
            return []

        # Optimization: Read only the last 'limit' lines by seeking backwards from the end.
        # This avoids loading the entire file into memory as history grows.
        lines: list[bytes] = []
        buffer_size = 4096

        with self.path.open("rb") as f:
            f.seek(0, os.SEEK_END)
            pointer = f.tell()
            buffer = b""

            while pointer > 0 and len(lines) <= limit:
                read_size = min(pointer, buffer_size)
                pointer -= read_size
                f.seek(pointer)
                buffer = f.read(read_size) + buffer

                new_lines = buffer.splitlines(keepends=True)
                if len(new_lines) > 1:
                    # The first element may be a partial line, so we keep it in the buffer.
                    # All other elements are complete lines.
                    lines = new_lines[1:] + lines
                    buffer = new_lines[0]

                if len(lines) > limit:
                    break

            # The remaining buffer is the very first (possibly partial) line of the file.
            if buffer and len(lines) < limit:
                lines = [buffer] + lines

        messages: list[Message] = []
        for line in lines[-limit:]:
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
