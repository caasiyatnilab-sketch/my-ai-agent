from my_ai_agent.tools import Calculator, WorkspaceReader


def test_calculator_dos_protection():
    calc = Calculator()
    # This would normally hang/consume lots of memory
    result = calc.run("10**1001")
    assert result.ok is False
    assert "Exponent too large" in result.output

    # Normal power operation should still work
    result = calc.run("2**10")
    assert result.ok is True
    assert result.output == "1024"

def test_workspace_reader_streaming(tmp_path):
    # Create a large file
    large_file = tmp_path / "large.txt"
    with open(large_file, "w") as f:
        f.write("A" * 10000)

    reader = WorkspaceReader(tmp_path)
    # Should only read up to max_chars
    result = reader.run("large.txt", max_chars=100)
    assert result.ok is True
    assert len(result.output) == 100
    assert result.output == "A" * 100
