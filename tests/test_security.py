from pathlib import Path
from my_ai_agent.tools import Calculator, WorkspaceReader

def test_calculator_exponent_limit():
    calc = Calculator()
    # Exponent just above the limit
    result = calc.run("2**1001")
    assert not result.ok
    assert "Exponent too large" in result.output

    # Exponent at the limit (should still be checked by magnitude)
    result = calc.run("2**1000")
    assert not result.ok
    assert "Result magnitude too large" in result.output

def test_calculator_magnitude_limit():
    calc = Calculator()
    # Multiplication result too large
    result = calc.run("10**60 * 10**60")
    assert not result.ok
    assert "Result magnitude too large" in result.output

    # Small result is OK
    result = calc.run("2**10")
    assert result.ok
    assert result.output == "1024"

def test_workspace_reader_safe_read(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    large_file = workspace / "large.txt"
    # Create a "large" file (larger than max_chars)
    large_file.write_text("A" * 10_000, encoding="utf-8")

    reader = WorkspaceReader(workspace)
    max_chars = 100
    result = reader.run("large.txt", max_chars=max_chars)

    assert result.ok
    assert len(result.output) == max_chars
    assert result.output == "A" * max_chars

def test_memory_loading_efficiency(tmp_path):
    from my_ai_agent.memory import JsonlMemory, Message
    memory_path = tmp_path / "large_memory.jsonl"
    memory = JsonlMemory(memory_path)

    # Write 100 lines
    for i in range(100):
        memory.append(Message("user", f"message {i}"))

    # Load last 5
    messages = memory.load(limit=5)
    assert len(messages) == 5
    assert messages[0].content == "message 95"
    assert messages[-1].content == "message 99"
