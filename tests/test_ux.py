from pathlib import Path
from my_ai_agent.tools import WorkspaceReader

def test_workspace_reader_truncation(tmp_path: Path) -> None:
    large_file = tmp_path / "large.txt"
    content = "Hello, World!"
    large_file.write_text(content, encoding="utf-8")

    reader = WorkspaceReader(tmp_path)
    # Test without truncation
    result = reader.run("large.txt", max_chars=20)
    assert result.ok
    assert result.output == content
    assert "[TRUNCATED" not in result.output

    # Test with truncation
    max_chars = 5
    result = reader.run("large.txt", max_chars=max_chars)
    assert result.ok
    assert result.output.startswith("Hello")
    assert f"[TRUNCATED: Only the first {max_chars} characters are shown]" in result.output
