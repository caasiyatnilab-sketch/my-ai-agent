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
        """Load the last `limit` messages from history.

        Optimized to read from the end of the file in chunks to avoid O(N) memory
        and time overhead for large history files.
        """
        if not self.path.exists():
            return []

        lines: list[str] = []
        chunk_size = 4096

        with self.path.open("rb") as f:
            f.seek(0, 2)  # Seek to end
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
                    buffer = parts[0]
                    new_lines = parts[1:]
                else:
                    new_lines = parts
                    buffer = b""

                for i in range(len(new_lines) - 1, -1, -1):
                    line = new_lines[i].strip()
                    if line:
                        lines.append(line.decode("utf-8"))
                        if len(lines) >= limit:
                            break

            if len(lines) < limit and buffer.strip():
                lines.append(buffer.strip().decode("utf-8"))

        messages: list[Message] = []
        # lines are in reverse order (newest first), so we reverse them back
        for line_str in reversed(lines[:limit]):
            try:
                data = json.loads(line_str)
                messages.append(Message(role=str(data["role"]), content=str(data["content"])))
            except (json.JSONDecodeError, KeyError):
                continue
        return messages

    def append(self, message: Message) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(asdict(message), ensure_ascii=False) + "\n")
