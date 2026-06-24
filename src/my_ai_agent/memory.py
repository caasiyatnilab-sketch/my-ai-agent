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

        # Security: Read only the end of the file to prevent OOM on large history
        # We'll read in chunks from the end.
        lines: list[str] = []
        chunk_size = 4096
        with self.path.open("rb") as f:
            f.seek(0, 2)
            file_size = f.tell()
            pointer = file_size
            buffer = bytearray()

            while len(lines) <= limit and pointer > 0:
                step = min(pointer, chunk_size)
                pointer -= step
                f.seek(pointer)
                chunk = f.read(step)
                buffer[:0] = chunk

                # Split buffer into lines
                while b"\n" in buffer and len(lines) <= limit:
                    last_newline = buffer.rfind(b"\n")
                    line = buffer[last_newline + 1 :].decode("utf-8")
                    if line.strip():
                        lines.append(line)
                    buffer = buffer[:last_newline]

            # Add the remaining buffer as the first line if it's not empty
            if len(lines) <= limit and buffer:
                line = buffer.decode("utf-8")
                if line.strip():
                    lines.append(line)

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
