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
        if not self.path.exists():
            return []

        # Performance: Read the file backwards to only load the last `limit` messages.
        # This avoids reading the entire conversation history into memory.
        lines: list[str] = []
        chunk_size = 4096
        with self.path.open("rb") as f:
            f.seek(0, 2)
            file_size = f.tell()
            pointer = file_size
            buffer = b""

            while pointer > 0 and len(lines) <= limit:
                step = min(pointer, chunk_size)
                pointer -= step
                f.seek(pointer)
                chunk = f.read(step) + buffer
                chunk_lines = chunk.split(b"\n")

                # The first element might be a partial line, keep it for the next iteration
                buffer = chunk_lines[0]

                # All other elements are complete lines (in reverse order)
                for i in range(len(chunk_lines) - 1, 0, -1):
                    if chunk_lines[i]:
                        lines.append(chunk_lines[i].decode("utf-8"))
                        if len(lines) >= limit:
                            break

            # Don't forget the very first line in the file
            if len(lines) < limit and buffer:
                lines.append(buffer.decode("utf-8"))

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
