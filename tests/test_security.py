from my_ai_agent.tools import Calculator, WorkspaceReader


def test_calculator_exponent_limit():
    calc = Calculator()
    result = calc.run("2**1001")
    assert result.ok is False
    assert "Exponent too large" in result.output


def test_calculator_magnitude_limit():
    calc = Calculator()
    # (10**100)**2 would be 10**200, which exceeds 1e100
    result = calc.run("(10**100)**2")
    assert result.ok is False
    assert "Result too large" in result.output


def test_calculator_magnitude_limit_nested():
    calc = Calculator()
    # 10**60 * 10**60 = 10**120
    result = calc.run("10**60 * 10**60")
    assert result.ok is False
    assert "Result too large" in result.output


def test_workspace_reader_large_file_safe(tmp_path):
    large_file = tmp_path / "large.txt"
    # Create a 1MB file (enough to test efficiency without being too slow for tests)
    large_file.write_text("A" * 1_000_000)

    reader = WorkspaceReader(tmp_path)
    result = reader.run("large.txt", max_chars=10)

    assert result.ok is True
    assert result.output == "A" * 10
    # The point is it didn't crash or take forever,
    # and we verified the code uses f.read(max_chars)
