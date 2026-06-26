from pathlib import Path
from my_ai_agent.tools import WorkspaceReader

def test_workspace_reader_binary_file(tmp_path: Path) -> None:
    binary_file = tmp_path / "binary.bin"
    binary_file.write_bytes(b"\xff\xfe\xfd")
    reader = WorkspaceReader(tmp_path)

    result = reader.run("binary.bin")

    assert result.ok is False
    assert result.output == "File contains non-UTF-8 data"

def test_workspace_reader_truncation_indicator(tmp_path: Path) -> None:
    large_file = tmp_path / "large.txt"
    large_file.write_text("A" * 100, encoding="utf-8")
    reader = WorkspaceReader(tmp_path)

    result = reader.run("large.txt", max_chars=10)

    assert result.ok is True
    assert "AAAAAAAAAA" in result.output
    assert "[... truncated ...]" in result.output
