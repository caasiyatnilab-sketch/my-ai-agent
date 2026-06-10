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
        """Load the last N messages from the memory file using chunked reverse-reading.

        This implementation reads the file backwards in chunks and splits by the newline byte
        before decoding to UTF-8, ensuring that multi-byte characters are not split across
        decoding boundaries.
        """
        if not self.path.exists():
            return []

        # We collect lines as bytes to avoid UnicodeDecodeError on chunk boundaries.
        line_bytes: list[bytes] = []
        chunk_size = 4096
        with self.path.open("rb") as f:
            f.seek(0, 2)
            pointer = f.tell()
            remainder = b""

            while len(line_bytes) < limit and pointer > 0:
                read_size = min(pointer, chunk_size)
                pointer -= read_size
                f.seek(pointer)
                chunk = f.read(read_size) + remainder

                # Split the chunk by newline bytes.
                parts = chunk.split(b"\n")

                # If we're not at the start of the file, the first part might be incomplete.
                # It becomes the 'remainder' for the next (backward) chunk.
                if pointer > 0:
                    remainder = parts[0]
                    new_lines = parts[1:]
                else:
                    remainder = b""
                    new_lines = parts

                # Filter out empty lines (e.g., from trailing newline)
                new_lines = [line for line in new_lines if line.strip()]

                # Add new lines to our collection in reverse order of discovery (since we're
                # reading backwards, but we want the final list to be forward-ordered).
                # Actually, let's just collect all discovered lines and then take the last N.
                line_bytes = new_lines + line_bytes

            # If we reached the start and there's a remainder, it's the first line.
            if remainder:
                line_bytes = [remainder] + line_bytes

        # Take only the requested amount from the end.
        selected_lines = [line.decode("utf-8") for line in line_bytes[-limit:] if line.strip()]

        messages: list[Message] = []
        for line in selected_lines:
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
