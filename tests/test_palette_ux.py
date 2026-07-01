from my_ai_agent.tools import WorkspaceReader


def test_workspace_reader_truncation_notice(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    large_file = workspace / "large.txt"
    content = "ABCDE" * 10  # 50 chars
    large_file.write_text(content, encoding="utf-8")

    reader = WorkspaceReader(workspace)
    # Test truncation at 10 chars
    result = reader.run("large.txt", max_chars=10)

    assert result.ok is True
    assert result.output.startswith("ABCDEABCDE")
    assert "... [truncated to 10 characters]" in result.output
    assert len(result.output) > 10

def test_workspace_reader_no_truncation_notice_when_small(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    small_file = workspace / "small.txt"
    content = "ABCDE"
    small_file.write_text(content, encoding="utf-8")

    reader = WorkspaceReader(workspace)
    result = reader.run("small.txt", max_chars=10)

    assert result.ok is True
    assert result.output == "ABCDE"
    assert "... [truncated" not in result.output
