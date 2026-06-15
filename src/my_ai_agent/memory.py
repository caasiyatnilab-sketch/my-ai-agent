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
        """Load recent messages from the end of the JSONL file without reading it entirely."""
        if not self.path.exists():
            return []

        # Read the last few kilobytes to find the requested number of lines
        # This is an optimization to avoid OOM on massive memory files.
        lines: list[str] = []
        chunk_size = 4096
        with self.path.open("rb") as f:
            f.seek(0, 2)
            file_size = f.tell()
            pointer = file_size
            while len(lines) <= limit and pointer > 0:
                pointer = max(0, pointer - chunk_size)
                f.seek(pointer)
                chunk = f.read(file_size - pointer if pointer == 0 else chunk_size)
                # Decode and split, keeping track of how many lines we have
                lines = chunk.decode("utf-8", errors="ignore").splitlines()
                # If we have enough lines, we can stop early
                if len(lines) > limit:
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
