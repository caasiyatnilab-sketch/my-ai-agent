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
        """Load the last N messages from history using binary backward seeking."""
        if not self.path.exists():
            return []

        messages: list[Message] = []
        chunk_size = 4096
        with self.path.open("rb") as f:
            f.seek(0, 2)
            pointer = f.tell()
            buffer = b""

            # Read backward in chunks until we have enough lines to satisfy the limit
            while pointer > 0:
                read_size = min(pointer, chunk_size)
                pointer -= read_size
                f.seek(pointer)
                buffer = f.read(read_size) + buffer
                if buffer.count(b"\n") > limit:
                    break

            lines = buffer.splitlines()
            for line in lines[-limit:]:
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
