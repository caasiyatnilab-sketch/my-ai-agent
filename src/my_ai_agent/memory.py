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
        """Load the last N messages from the memory file using efficient reverse reading."""
        if not self.path.exists():
            return []

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
                buffer = f.read(step) + buffer
                # Split and count lines from the buffer
                current_lines = buffer.split(b"\n")
                if len(current_lines) > 1:
                    # Keep the first partial line for the next iteration
                    buffer = current_lines[0]
                    # The rest are complete lines (in reverse order)
                    for i in range(len(current_lines) - 1, 0, -1):
                        line = current_lines[i].decode("utf-8").strip()
                        if line:
                            lines.append(line)
                            if len(lines) >= limit:
                                break
            # Handle any remaining buffer
            if len(lines) < limit and buffer:
                line = buffer.decode("utf-8").strip()
                if line:
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
