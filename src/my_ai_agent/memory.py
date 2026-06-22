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
        """Load the latest messages from the JSONL file without reading the whole file."""
        if not self.path.exists():
            return []

        lines: list[str] = []
        try:
            with self.path.open("rb") as f:
                f.seek(0, 2)
                file_size = f.tell()
                buffer = bytearray()
                pointer = file_size
                chunk_size = 4096

                while pointer > 0 and len(lines) < limit:
                    seek_pos = max(0, pointer - chunk_size)
                    f.seek(seek_pos)
                    chunk = f.read(pointer - seek_pos)
                    buffer = chunk + buffer
                    pointer = seek_pos

                    while b"\n" in buffer and len(lines) < limit:
                        newline_pos = buffer.rfind(b"\n")
                        line_bytes = buffer[newline_pos + 1 :].strip()
                        if line_bytes:
                            lines.append(line_bytes.decode("utf-8"))
                        buffer = buffer[:newline_pos]

                # Handle the first line if we reached the start of the file
                if pointer == 0 and len(lines) < limit and buffer.strip():
                    lines.append(buffer.decode("utf-8"))
        except OSError:
            return []

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
