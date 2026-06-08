from my_ai_agent.tools import Calculator, WorkspaceReader


def test_calculator_exponent_limit():
    calc = Calculator()
    # Safe exponent
    result = calc.run("2**1000")
    assert result.ok is True

    # Over limit
    result = calc.run("2**1001")
    assert result.ok is False
    assert "Exponent too large" in result.output

def test_calculator_nested_exponent_limit():
    calc = Calculator()
    # (2**10)**10 = 2**100, safe
    result = calc.run("(2**10)**10")
    assert result.ok is True

    # 2**(2**10) = 2**1024, over limit
    result = calc.run("2**(2**10)")
    assert result.ok is False
    assert "Exponent too large" in result.output

def test_workspace_reader_bounded_read(tmp_path):
    # Create a large file
    large_file = tmp_path / "large.txt"
    content = "A" * 10_000
    large_file.write_text(content, encoding="utf-8")

    reader = WorkspaceReader(tmp_path)
    # Default max_chars is 8000
    result = reader.run("large.txt")
    assert result.ok is True
    assert len(result.output) == 8000
    assert result.output == "A" * 8000

    # Custom max_chars
    result = reader.run("large.txt", max_chars=100)
    assert result.ok is True
    assert len(result.output) == 100
    assert result.output == "A" * 100
