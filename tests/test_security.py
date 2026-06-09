from pathlib import Path

from my_ai_agent.tools import Calculator, WorkspaceReader


def test_calculator_exponent_limit():
    calc = Calculator()
    result = calc.run("10**1001")
    assert result.ok is False
    assert "Exponent too large" in result.output


def test_calculator_magnitude_limit():
    calc = Calculator()
    # 10**309 should exceed 1e308
    result = calc.run("10**309")
    assert result.ok is False
    assert "Result too large" in result.output


def test_calculator_nested_exponent_limit():
    calc = Calculator()
    # (10**2)**100 is 10**200, which is fine (< 1e308)
    result = calc.run("(10**2)**100")
    assert result.ok is True

    # (10**10)**100 is 10**1000, which is > 1e308
    result = calc.run("(10**10)**100")
    assert result.ok is False
    assert "Result too large" in result.output


def test_workspace_reader_large_file_safe(tmp_path: Path):
    large_file = tmp_path / "large.txt"
    # Create a 1MB file
    large_file.write_text("A" * 1024 * 1024, encoding="utf-8")

    reader = WorkspaceReader(tmp_path)
    # Should only read up to max_chars (default 8000)
    result = reader.run("large.txt")
    assert result.ok is True
    assert len(result.output) == 8000
