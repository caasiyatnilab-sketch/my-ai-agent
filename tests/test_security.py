import pytest
from pathlib import Path
from my_ai_agent.tools import Calculator, WorkspaceReader

def test_calculator_exponent_limit():
    calc = Calculator()
    # Large exponent should be rejected
    result = calc.run("2**1001")
    assert not result.ok
    assert "too large" in result.output.lower()

def test_calculator_magnitude_limit():
    calc = Calculator()
    # Result magnitude should be limited
    result = calc.run("10**100")
    assert result.ok # 1e100 is my planned limit

    result = calc.run("10**101")
    assert not result.ok
    assert "too large" in result.output.lower()

def test_workspace_reader_memory_safe(tmp_path):
    # Create a large file
    large_file = tmp_path / "large.txt"
    with open(large_file, "wb") as f:
        f.write(b"A" * 1024 * 1024) # 1MB

    reader = WorkspaceReader(tmp_path)
    # Reading with small max_chars should be fast and not load everything
    result = reader.run("large.txt", max_chars=10)
    assert result.ok
    assert len(result.output) == 10
    assert result.output == "A" * 10
