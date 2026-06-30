"""Simple JSONL conversation memory."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path

from .providers import Message


class JsonlMemory:
    """Append-only conversation memory suitable for local CLI usage."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self, limit: int = 20) -> list[Message]:
        """Load the last N messages from memory using backward seeking for performance."""
        if not self.path.exists():
            return []

        lines: list[bytes] = []
        chunk_size = 4096

        # Efficiently read only the end of the file in chunks
        with self.path.open("rb") as f:
            f.seek(0, 2)  # SEEK_END
            pointer = f.tell()
            buffer = b""

            while pointer > 0 and len(lines) <= limit:
                seek_pos = max(0, pointer - chunk_size)
                f.seek(seek_pos)
                chunk = f.read(pointer - seek_pos)
                pointer = seek_pos

                chunk_with_buffer = chunk + buffer
                chunk_lines = chunk_with_buffer.splitlines(keepends=True)

                # If we're not at the start of the file, the first line might be incomplete
                if pointer > 0 and not chunk_with_buffer.startswith((b"\n", b"\r")):
                    buffer = chunk_lines.pop(0)
                else:
                    buffer = b""

                lines.extend(reversed(chunk_lines))

        messages: list[Message] = []
        for line in lines:
            if not line.strip():
                continue
            try:
                data = json.loads(line.decode("utf-8"))
                messages.append(Message(role=str(data["role"]), content=str(data["content"])))
                if len(messages) >= limit:
                    break
            except (json.JSONDecodeError, KeyError):
                continue

        return list(reversed(messages))

    def append(self, message: Message) -> None:
        """Append a message to memory. Uses __dict__ for faster serialization than asdict()."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            # message.__dict__ is faster than asdict(message) for simple dataclasses
            stream.write(json.dumps(message.__dict__, ensure_ascii=False) + "\n")
