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
        lines: list[str] = []
        chunk_size = 4096
        with self.path.open("rb") as f:
            f.seek(0, 2)
            pointer = f.tell()
            buffer = b""
            while pointer > 0 and len(lines) < limit:
                step = min(pointer, chunk_size)
                pointer -= step
                f.seek(pointer)
                chunk = f.read(step) + buffer
                # Split by newline and handle the last potentially incomplete line in the buffer
                parts = chunk.split(b"\n")
                if pointer > 0:
                    buffer = parts[0]
                    lines_in_chunk = [p.decode("utf-8").strip() for p in parts[1:] if p.strip()]
                else:
                    buffer = b""
                    lines_in_chunk = [p.decode("utf-8").strip() for p in parts if p.strip()]

                # Prepend lines found in this chunk
                lines = lines_in_chunk + lines

            # If we have too many lines, take the last 'limit' ones
            if len(lines) > limit:
                lines = lines[-limit:]

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
