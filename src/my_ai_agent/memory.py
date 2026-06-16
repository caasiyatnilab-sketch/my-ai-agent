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
        """Load the last N messages from memory using efficient reverse file reading."""

        if not self.path.exists():
            return []

        lines: list[str] = []
        chunk_size = 4096
        with self.path.open("rb") as f:
            f.seek(0, os.SEEK_END)
            file_size = f.tell()
            pointer = file_size
            buffer = b""

            while pointer > 0 and len(lines) < limit:
                read_size = min(pointer, chunk_size)
                pointer -= read_size
                f.seek(pointer)
                chunk = f.read(read_size)
                buffer = chunk + buffer

                # Split lines by newline byte. We ignore the very last character if it's a newline
                # because splitlines() also ignores a trailing newline.
                # However, since we're reading backwards, it's easier to just split and manage.
                current_lines = buffer.split(b"\n")

                # The first element might be incomplete unless pointer is 0
                if pointer > 0:
                    buffer = current_lines[0]
                    current_chunk_lines = current_lines[1:]
                else:
                    buffer = b""
                    current_chunk_lines = current_lines

                # Filter out empty strings that occur due to trailing newlines
                # but only if it's the very last line of the file.
                if (
                    pointer + read_size == file_size
                    and current_chunk_lines
                    and not current_chunk_lines[-1]
                ):
                    current_chunk_lines.pop()

                for line_bytes in reversed(current_chunk_lines):
                    if len(lines) < limit:
                        lines.append(line_bytes.decode("utf-8"))
                    else:
                        break

        messages: list[Message] = []
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
