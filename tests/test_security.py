
from my_ai_agent.tools import Calculator, WorkspaceReader


def test_calculator_dos_exponentiation():
    calc = Calculator()
    # Large exponentiation can cause DoS
    result = calc.run("10**1000000")
    assert not result.ok
    assert "too large" in result.output.lower() or "invalid" in result.output.lower()

def test_calculator_dos_multiplication():
    calc = Calculator()
    # Large multiplication can also be problematic
    # We use large numbers to try and trigger resource exhaustion
    result = calc.run("(10**1000) * (10**1000)")
    assert not result.ok
    assert "too large" in result.output.lower() or "invalid" in result.output.lower()

def test_workspacereader_oom_mitigation(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    large_file = workspace / "large.txt"

    # Create a 1MB file (enough for testing logic without being too slow)
    content = "A" * 1_000_000
    large_file.write_text(content, encoding="utf-8")

    reader = WorkspaceReader(workspace)
    # We want to ensure that reading 100 chars doesn't load 1MB
    # This is hard to assert directly without mocking open(),
    # but we can at least verify it works for small max_chars.
    result = reader.run("large.txt", max_chars=100)
    assert result.ok
    assert len(result.output) == 100
    assert result.output == "A" * 100

def test_workspacereader_path_traversal(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (workspace / "allowed.txt").write_text("allowed", encoding="utf-8")

    reader = WorkspaceReader(workspace)

    # Test path traversal attempts
    assert not reader.run("../test.txt").ok
    assert not reader.run("/etc/passwd").ok
