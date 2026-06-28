import pytest
import json
from pathlib import Path
from my_ai_agent.tools import Calculator, WorkspaceReader
from my_ai_agent.memory import JsonlMemory
from my_ai_agent.providers import Message

def test_calculator_dos_exponent():
    calc = Calculator()
    result = calc.run("1.1**1001")
    assert not result.ok
    assert "exponent too large" in result.output.lower()

def test_calculator_dos_multiplication():
    calc = Calculator()
    expr = f"{(10**2000)} * {(10**2000)}"
    result = calc.run(expr)
    assert not result.ok
    assert "multiplication result too large" in result.output.lower()

def test_calculator_dos_result_magnitude():
    calc = Calculator()
    result = calc.run("10**1000")
    assert not result.ok
    assert "result too large" in result.output.lower()

def test_workspacereader_oom_protection(tmp_path):
    large_file = tmp_path / "large.txt"
    with open(large_file, "wb") as f:
        f.seek(10 * 1024 * 1024 - 1)
        f.write(b"\0")

    reader = WorkspaceReader(tmp_path)
    import time
    start = time.time()
    result = reader.run("large.txt", max_chars=100)
    duration = time.time() - start

    assert result.ok
    assert len(result.output) <= 100
    assert duration < 0.1

def test_jsonlmemory_oom_protection(tmp_path):
    history_file = tmp_path / "history.jsonl"
    line = json.dumps({"role": "user", "content": "hello"}) + "\n"
    with open(history_file, "w") as f:
        for _ in range(50000):
            f.write(line)

    memory = JsonlMemory(history_file)
    import time
    start = time.time()
    messages = memory.load(limit=20)
    duration = time.time() - start

    assert len(messages) == 20
    assert duration < 0.1
