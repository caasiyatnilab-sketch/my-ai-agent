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
        """Load the last N messages from memory using efficient reverse-file reading."""
        if not self.path.exists():
            return []

        lines: list[str] = []
        chunk_size = 4096

        # Efficiently read the file from the end in chunks to avoid loading the entire
        # file into memory. This is O(limit) instead of O(total_lines).
        try:
            with self.path.open("rb") as f:
                f.seek(0, 2)
                file_size = f.tell()
                pointer = file_size

                # If the file ends with a newline, splitlines() ignores it as a line terminator.
                # We mimic this by skipping the very last byte if it's a newline.
                if pointer > 0:
                    f.seek(pointer - 1)
                    if f.read(1) == b"\n":
                        pointer -= 1

                buffer = b""
                while pointer > 0 and len(lines) < limit:
                    read_size = min(pointer, chunk_size)
                    pointer -= read_size
                    f.seek(pointer)
                    chunk = f.read(read_size)
                    buffer = chunk + buffer

                    while b"\n" in buffer and len(lines) < limit:
                        newline_pos = buffer.rfind(b"\n")
                        # Extract line, decode, and strip potential carriage return
                        line = buffer[newline_pos + 1 :].decode("utf-8").rstrip("\r")
                        lines.append(line)
                        buffer = buffer[:newline_pos]

                # Add the remaining buffer as the first line of the file
                if len(lines) < limit and (buffer or (file_size > 0 and not lines)):
                    lines.append(buffer.decode("utf-8").rstrip("\r"))
        except OSError:
            return []

        messages: list[Message] = []
        # lines were collected from end to start, so reverse them back
        for line in reversed(lines):
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
