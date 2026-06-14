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
        """Load the last N messages using an efficient reverse-read strategy."""
        if not self.path.exists() or limit <= 0:
            return []

        lines: list[bytes] = []
        chunk_size = 4096
        with self.path.open("rb") as f:
            f.seek(0, 2)
            file_size = f.tell()
            pointer = file_size
            buffer = b""

            while pointer > 0 and len(lines) < limit:
                read_size = min(pointer, chunk_size)
                pointer -= read_size
                f.seek(pointer)
                chunk = f.read(read_size) + buffer
                # splitlines() on bytes works similar to str.splitlines()
                # We need to handle the case where the first line of the chunk is incomplete.
                parts = chunk.split(b"\n")

                if pointer > 0:
                    # The first part is likely incomplete, keep for next iteration.
                    buffer = parts[0]
                    # The rest are complete lines (or empty if the chunk ended with \n)
                    current_lines = parts[1:]
                else:
                    # At the start of the file, all parts are complete.
                    buffer = b""
                    current_lines = parts

                # Process lines from the end of current_lines backwards.
                for i in range(len(current_lines) - 1, -1, -1):
                    # Skip empty lines at the very end of the file.
                    is_at_end = (
                        pointer + len(buffer) + sum(len(p) + 1 for p in current_lines[: i + 1])
                        >= file_size
                    )
                    if not current_lines[i] and is_at_end:
                        continue
                    lines.append(current_lines[i])
                    if len(lines) >= limit:
                        break

            if buffer and len(lines) < limit:
                lines.append(buffer)

        messages: list[Message] = []
        # lines were collected in reverse order (last line first), so we reverse back.
        for raw_line in reversed(lines):
            line = raw_line.decode("utf-8").strip()
            if not line:
                continue
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
