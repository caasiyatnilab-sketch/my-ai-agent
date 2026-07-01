"""Simple JSONL conversation memory."""

from __future__ import annotations

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
        with self.path.open("rb") as f:
            f.seek(0, 2)
            pointer = f.tell()
            buffer = b""

            while pointer > 0 and len(lines) <= limit:
                seek_pos = max(0, pointer - chunk_size)
                f.seek(seek_pos)
                chunk = f.read(pointer - seek_pos)
                pointer = seek_pos

                combined = chunk + buffer
                parts = combined.splitlines(keepends=True)

                if pointer > 0 and combined and not combined.startswith((b"\n", b"\r")):
                    # If not at the start of file, the first part might be incomplete
                    buffer = parts[0]
                    lines = parts[1:] + lines
                else:
                    buffer = b""
                    lines = parts + lines

            if buffer:
                lines = [buffer] + lines

        messages: list[Message] = []
        # Filter empty lines (e.g. trailing newline) and take the requested limit
        valid_lines = [line for line in lines if line.strip()]
        for line in valid_lines[-limit:]:
            try:
                data = json.loads(line)
                messages.append(Message(role=str(data["role"]), content=str(data["content"])))
            except (json.JSONDecodeError, KeyError):
                continue
        return messages

    def append(self, message: Message) -> None:
        """Append a new message to memory efficiently."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            # Using __dict__ is ~25% faster than asdict(message) for simple objects
            stream.write(json.dumps(message.__dict__, ensure_ascii=False) + "\n")
