import pytest
from pathlib import Path
from my_ai_agent.tools import Calculator, WorkspaceReader
import time

def test_calculator_dos_exponent():
    calc = Calculator()
    result = calc.run("10**1001")
    assert result.ok is False
    assert "Exponent too large" in result.output

def test_calculator_dos_multiplication():
    calc = Calculator()
    # 2**5000 has bit_length slightly above 5000.
    # (2**5000) * (2**5001) should have combined bit_length > 10000
    expr = f"({2**5000}) * ({2**5001})"
    result = calc.run(expr)
    assert result.ok is False
    assert "Multiplication operands too large" in result.output

def test_calculator_magnitude_limit():
    calc = Calculator()
    result = calc.run("10**101")
    assert result.ok is False
    assert "magnitude" in result.output

def test_workspacereader_oom_mitigation(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    large_file = workspace / "large.txt"

    # 100MB file
    content = "A" * (100 * 1024 * 1024)
    large_file.write_text(content, encoding="utf-8")

    reader = WorkspaceReader(workspace)

    # We want to measure memory or just ensure it doesn't read everything.
    # Mocking read_text might be easier to verify it's NOT called if we change the implementation.
    # Or just verify it works efficiently.
    start = time.time()
    result = reader.run("large.txt", max_chars=100)
    duration = time.time() - start

    assert result.ok is True
    assert len(result.output) == 100
    print(f"WorkspaceReader took {duration:.4f}s for 100MB file")
