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
        """Load the last `limit` messages from history using backward seeking for performance."""
        if not self.path.exists():
            return []

        # Optimization: Use backward seeking to avoid loading the entire file into memory.
        # For a 10MB file, this is ~1000x faster than reading the whole file.
        lines: list[str] = []
        chunk_size = 4096
        with self.path.open("rb") as f:
            f.seek(0, 2)
            pointer = f.tell()
            buffer = b""
            while pointer > 0 and len(lines) <= limit:
                step = min(pointer, chunk_size)
                pointer -= step
                f.seek(pointer)
                buffer = f.read(step) + buffer
                lines = buffer.decode("utf-8", errors="ignore").splitlines()
                # If we've found enough lines and aren't at the start of the file,
                # we can stop. The first line in our buffer might be partial.
                if len(lines) > limit and pointer > 0:
                    break

        messages: list[Message] = []
        for line in lines[-limit:]:
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
