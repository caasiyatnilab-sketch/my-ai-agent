from pathlib import Path

from my_ai_agent.tools import Calculator, WorkspaceReader


def test_calculator_dos_exponent():
    calc = Calculator()
    # Large exponent should be caught before execution or result in an error
    # Instead of 'Killed', it should return an error result
    result = calc.run("2**1000000")
    assert result.ok is False
    assert "too large" in result.output.lower() or "limit" in result.output.lower()


def test_calculator_dos_nested_exponent():
    calc = Calculator()
    # Nested exponents can bypass simple checks if not careful
    result = calc.run("2**2**100")
    assert result.ok is False
    assert "too large" in result.output.lower() or "limit" in result.output.lower()


def test_workspace_reader_memory_safe_read(tmp_path: Path):
    # Create a large file
    large_file = tmp_path / "large.txt"
    with open(large_file, "w") as f:
        f.write("A" * 1_000_000)

    reader = WorkspaceReader(tmp_path)
    # Reading should be fast and not load the whole file into memory
    result = reader.run("large.txt", max_chars=100)
    assert result.ok is True
    assert "TRUNCATED" in result.output
    assert result.output.startswith("A" * 100)
