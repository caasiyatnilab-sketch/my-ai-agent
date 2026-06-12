from my_ai_agent.tools import Calculator, WorkspaceReader


def test_calculator_exponent_limit():
    calc = Calculator()
    # This should fail gracefully rather than hanging or throwing a system-level error
    result = calc.run("2**1000000")
    assert result.ok is False
    assert "exceeds" in result.output.lower() or "maximum" in result.output.lower()


def test_calculator_magnitude_limit():
    calc = Calculator()
    # Nested power to bypass simple exponent check
    result = calc.run("(10**100)**100")
    assert result.ok is False
    assert "exceeds" in result.output.lower() or "maximum" in result.output.lower()


def test_workspace_reader_memory_safety(tmp_path):
    # Create a large file
    large_file = tmp_path / "large.txt"
    with open(large_file, "wb") as f:
        f.write(b"a" * 1_000_000)

    reader = WorkspaceReader(tmp_path)
    # Even with a small max_chars, it shouldn't read the whole 1MB into memory
    # We can't easily measure memory here, but we can check if it works
    result = reader.run("large.txt", max_chars=100)
    assert result.ok is True
    assert len(result.output) == 100
