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
        """Load the last N messages from history using efficient reverse seeking."""
        if not self.path.exists():
            return []

        lines: list[str] = []
        buffer_size = 4096
        with self.path.open("rb") as f:
            f.seek(0, 2)
            file_size = f.tell()
            pos = file_size
            buffer = b""

            while pos > 0 and len(lines) <= limit:
                read_size = min(pos, buffer_size)
                pos -= read_size
                f.seek(pos)
                chunk = f.read(read_size)
                buffer = chunk + buffer

                # Split and handle partial lines
                while b"\n" in buffer and len(lines) <= limit:
                    # Find last newline
                    last_newline = buffer.rfind(b"\n")
                    line = buffer[last_newline + 1 :].decode("utf-8").strip()
                    if line:
                        lines.append(line)
                    buffer = buffer[:last_newline]

            # Add any remaining text in buffer as the first line if we still need more lines
            if len(lines) < limit:
                line = buffer.decode("utf-8").strip()
                if line:
                    lines.append(line)

        # We collected lines from end to start, so reverse them to get chronological order
        # and slice to exactly the limit requested.
        messages: list[Message] = []
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
