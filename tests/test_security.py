from my_ai_agent.tools import Calculator, WorkspaceReader


def test_calculator_exponent_limit():
    calc = Calculator()
    # Direct large exponent
    result = calc.run("2**1001")
    assert not result.ok
    assert "Exponent too large" in result.output

    # Nested large exponent that could still be large but bypassed simple checks
    # (2**10)**200 = 2**2000
    result = calc.run("(2**10)**200")
    assert not result.ok
    assert "Exponent too large" in result.output or "Result too large" in result.output


def test_calculator_magnitude_limit():
    calc = Calculator()
    result = calc.run("10**101")
    assert not result.ok
    assert "Result too large" in result.output


def test_workspace_reader_limited_read(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    large_file = workspace / "large.txt"
    large_file.write_text("A" * 10000)

    reader = WorkspaceReader(workspace)
    # Read only 10 chars
    result = reader.run("large.txt", max_chars=10)
    assert result.ok
    assert len(result.output) == 10
    assert result.output == "A" * 10
