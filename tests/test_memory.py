
import json
from pathlib import Path
import pytest
from my_ai_agent.memory import JsonlMemory
from my_ai_agent.providers import Message

@pytest.fixture
def memory_file(tmp_path):
    return tmp_path / "test_memory.jsonl"

def test_load_empty_file(memory_file):
    memory = JsonlMemory(memory_file)
    assert memory.load() == []

def test_load_nonexistent_file(tmp_path):
    memory = JsonlMemory(tmp_path / "nonexistent.jsonl")
    assert memory.load() == []

def test_append_and_load(memory_file):
    memory = JsonlMemory(memory_file)
    msg1 = Message("user", "hello")
    msg2 = Message("assistant", "hi")

    memory.append(msg1)
    memory.append(msg2)

    loaded = memory.load()
    assert len(loaded) == 2
    assert loaded[0] == msg1
    assert loaded[1] == msg2

def test_load_with_limit(memory_file):
    memory = JsonlMemory(memory_file)
    for i in range(10):
        memory.append(Message("user", f"msg {i}"))

    loaded = memory.load(limit=3)
    assert len(loaded) == 3
    assert loaded[0].content == "msg 7"
    assert loaded[1].content == "msg 8"
    assert loaded[2].content == "msg 9"

def test_load_with_limit_larger_than_file(memory_file):
    memory = JsonlMemory(memory_file)
    for i in range(5):
        memory.append(Message("user", f"msg {i}"))

    loaded = memory.load(limit=10)
    assert len(loaded) == 5
    assert loaded[0].content == "msg 0"
    assert loaded[-1].content == "msg 4"

def test_load_with_corrupt_json(memory_file):
    memory = JsonlMemory(memory_file)
    memory.append(Message("user", "valid"))

    with memory_file.open("a", encoding="utf-8") as f:
        f.write("invalid json\n")

    memory.append(Message("assistant", "also valid"))

    loaded = memory.load()
    assert len(loaded) == 2
    assert loaded[0].content == "valid"
    assert loaded[1].content == "also valid"

def test_load_large_file_efficiency(memory_file):
    memory = JsonlMemory(memory_file)
    # Write a lot of data
    with memory_file.open("w", encoding="utf-8") as f:
        for i in range(1000):
            f.write(json.dumps({"role": "user", "content": "x" * 100}) + "\n")

    # Last message
    last_msg = Message("assistant", "last one")
    memory.append(last_msg)

    loaded = memory.load(limit=1)
    assert len(loaded) == 1
    assert loaded[0] == last_msg

def test_load_trailing_newline(memory_file):
    memory = JsonlMemory(memory_file)
    memory.append(Message("user", "hello"))
    # Ensure there is a trailing newline (append does this)

    loaded = memory.load(limit=1)
    assert len(loaded) == 1
    assert loaded[0].content == "hello"

def test_load_no_trailing_newline(memory_file):
    memory = JsonlMemory(memory_file)
    msg = Message("user", "hello")
    with memory_file.open("w", encoding="utf-8") as f:
        f.write(json.dumps(msg.__dict__))

    loaded = memory.load(limit=1)
    assert len(loaded) == 1
    assert loaded[0].content == "hello"
