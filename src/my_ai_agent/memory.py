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

        lines: list[bytes] = []
        chunk_size = 4096

        with self.path.open("rb") as f:
            f.seek(0, 2)
            file_size = f.tell()
            pointer = file_size
            buffer = b""

            # If the file ends with a newline, skip it to mimic splitlines()
            if pointer > 0:
                f.seek(pointer - 1)
                if f.read(1) == b"\n":
                    pointer -= 1

            while pointer > 0 and len(lines) < limit:
                read_size = min(pointer, chunk_size)
                pointer -= read_size
                f.seek(pointer)
                chunk = f.read(read_size)
                buffer = chunk + buffer

                while b"\n" in buffer and len(lines) < limit:
                    newline_pos = buffer.rfind(b"\n")
                    line = buffer[newline_pos + 1 :]
                    lines.append(line)
                    buffer = buffer[:newline_pos]

            if len(lines) < limit and buffer:
                lines.append(buffer)

        messages: list[Message] = []
        # lines are collected from end to start, so reverse them to restore order
        for line_bytes in reversed(lines):
            try:
                # Strip \r for cross-platform compatibility and decode
                line = line_bytes.decode("utf-8").rstrip("\r")
                if not line:
                    continue
                data = json.loads(line)
                messages.append(Message(role=str(data["role"]), content=str(data["content"])))
            except (json.JSONDecodeError, KeyError, UnicodeDecodeError):
                continue
        return messages

    def append(self, message: Message) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(asdict(message), ensure_ascii=False) + "\n")
