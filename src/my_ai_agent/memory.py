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
        """Load the last n messages from the history file using binary seeking for performance."""
        if not self.path.exists() or self.path.stat().st_size == 0:
            return []

        lines: list[str] = []
        chunk_size = 4096
        try:
            with self.path.open("rb") as f:
                f.seek(0, 2)
                pointer = f.tell()
                buffer = b""

                while pointer > 0 and len(lines) < limit:
                    step = min(pointer, chunk_size)
                    pointer -= step
                    f.seek(pointer)
                    chunk = f.read(step)
                    buffer = chunk + buffer

                    parts = buffer.split(b"\n")
                    if pointer > 0:
                        # Keep the first part in the buffer as it might be an incomplete line
                        buffer = parts[0]
                        # The remaining parts are complete lines
                        new_lines = [p.decode("utf-8") for p in parts[1:] if p]
                        lines = new_lines + lines
                    else:
                        # At the start of the file, all parts are complete lines
                        new_lines = [p.decode("utf-8") for p in parts if p]
                        lines = new_lines + lines

                if len(lines) > limit:
                    lines = lines[-limit:]
        except (OSError, UnicodeDecodeError):
            return []

        messages: list[Message] = []
        for line in lines:
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
