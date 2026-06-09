"""Simple JSONL conversation memory."""

from __future__ import annotations

from dataclasses import asdict
import json
import os
from pathlib import Path

from .providers import Message


class JsonlMemory:
    """Append-only conversation memory suitable for local CLI usage."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self, limit: int = 20) -> list[Message]:
        if not self.path.exists():
            return []

        lines: list[bytes] = []
        chunk_size = 4096

        with self.path.open("rb") as f:
            f.seek(0, os.SEEK_END)
            file_size = f.tell()
            pointer = file_size
            buffer = b""

            while pointer > 0 and len(lines) <= limit:
                read_size = min(pointer, chunk_size)
                pointer -= read_size
                f.seek(pointer)
                chunk = f.read(read_size)

                # Combine with leftover from previous read (which was actually 'next' in file)
                current_block = chunk + buffer
                block_lines = current_block.splitlines(keepends=True)

                # If we're not at the start of the file, the first line in block_lines
                # might be incomplete
                if pointer > 0:
                    buffer = block_lines[0]
                    lines_to_add = block_lines[1:]
                else:
                    buffer = b""
                    lines_to_add = block_lines

                # We want the lines in reverse order of discovery (last lines first)
                # but splitlines keeps order. We'll reverse the addition.
                lines.extend(reversed(lines_to_add))

        # Filter out empty lines (like trailing newline at end of file)
        # and take only the requested limit.
        final_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped:
                final_lines.append(stripped)
            if len(final_lines) == limit:
                break

        # Reverse back to chronological order
        final_lines.reverse()

        messages: list[Message] = []
        for line_bytes in final_lines:
            try:
                data = json.loads(line_bytes.decode("utf-8"))
                messages.append(Message(role=str(data["role"]), content=str(data["content"])))
            except (json.JSONDecodeError, KeyError, UnicodeDecodeError):
                continue
        return messages

    def append(self, message: Message) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(asdict(message), ensure_ascii=False) + "\n")
