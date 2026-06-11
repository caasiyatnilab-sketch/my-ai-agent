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

        lines: list[bytes] = []
        chunk_size = 4096

        # Optimize: Read file in reverse chunks to avoid loading the entire file into memory.
        # This is particularly effective for large history files when we only need the last N lines.
        with self.path.open("rb") as f:
            f.seek(0, os.SEEK_END)
            file_size = f.tell()
            offset = file_size

            while offset > 0 and len(lines) <= limit:
                read_size = min(offset, chunk_size)
                offset -= read_size
                f.seek(offset)
                chunk = f.read(read_size)

                # Split chunk by newline byte (0x0A).
                # 0x0A is safe for UTF-8 as it never appears as a non-leading byte in
                # multi-byte sequences.
                chunk_lines = chunk.split(b"\n")

                if not lines:
                    # First chunk read from the end. If it ends with a newline,
                    # the last element is empty.
                    if chunk_lines and chunk_lines[-1] == b"":
                        chunk_lines.pop()
                else:
                    # Stitch the split line across chunk boundaries.
                    if chunk_lines:
                        lines[0] = chunk_lines.pop() + lines[0]

                if chunk_lines:
                    lines = chunk_lines + lines

        messages: list[Message] = []
        # Process the collected lines from the end up to the limit.
        for line in lines[-limit:]:
            if not line:
                continue
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
