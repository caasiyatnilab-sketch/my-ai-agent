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
        """Load the last `limit` messages from the JSONL file by reading backwards."""
        if not self.path.exists():
            return []

        lines: list[str] = []
        chunk_size = 4096
        with self.path.open("rb") as f:
            f.seek(0, 2)
            size = f.tell()
            pointer = size
            remainder = b""

            while pointer > 0 and len(lines) < limit:
                read_size = min(pointer, chunk_size)
                pointer -= read_size
                f.seek(pointer)
                chunk = f.read(read_size) + remainder

                if pointer + read_size == size:
                    chunk = chunk.rstrip(b"\r\n")

                parts = chunk.split(b"\n")
                if pointer > 0:
                    remainder = parts[0]
                    current_lines = parts[1:]
                else:
                    remainder = b""
                    current_lines = parts

                for line_bytes in reversed(current_lines):
                    if len(lines) < limit:
                        # Strip carriage returns and decode
                        lines.append(line_bytes.decode("utf-8").replace("\r", ""))
                    else:
                        break

            if remainder and len(lines) < limit:
                lines.append(remainder.decode("utf-8").replace("\r", ""))

        lines.reverse()

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
