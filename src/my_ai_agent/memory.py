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
        """Load the last N messages from the memory file using reverse reading."""
        if not self.path.exists():
            return []

        lines: list[str] = []
        chunk_size = 4096

        # Optimization: Read file from the end in chunks to avoid O(n) memory/time
        # for large files when we only need the last few lines.
        with self.path.open("rb") as f:
            f.seek(0, 2)
            file_size = f.tell()
            pointer = file_size
            buffer = b""

            while pointer > 0 and len(lines) <= limit:
                read_size = min(pointer, chunk_size)
                pointer -= read_size
                f.seek(pointer)
                chunk = f.read(read_size)
                buffer = chunk + buffer

                # Extract lines from the end of the buffer
                while b"\n" in buffer and len(lines) <= limit:
                    index = buffer.rfind(b"\n")
                    line_bytes = buffer[index + 1 :]
                    if line_bytes.strip():
                        lines.append(line_bytes.decode("utf-8", errors="replace"))
                    buffer = buffer[:index]

            # Handle the first line in the file if it doesn't start with a newline
            if pointer == 0 and len(lines) <= limit and buffer.strip():
                lines.append(buffer.decode("utf-8", errors="replace"))

        messages: list[Message] = []
        # We collected lines from bottom to top, so reverse them back to chronological order.
        for line in reversed(lines[:limit]):
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
