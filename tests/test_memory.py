import json
from pathlib import Path
import pytest
from my_ai_agent.memory import JsonlMemory
from my_ai_agent.providers import Message

@pytest.fixture
def memory_path(tmp_path):
    return tmp_path / "test_memory.jsonl"

def test_load_empty_file(memory_path):
    memory = JsonlMemory(memory_path)
    assert memory.load() == []

def test_load_nonexistent_file(memory_path):
    memory = JsonlMemory(memory_path)
    assert memory.load() == []

def test_load_small_file(memory_path):
    memory = JsonlMemory(memory_path)
    messages = [
        Message(role="user", content="hello"),
        Message(role="assistant", content="hi"),
    ]
    for m in messages:
        memory.append(m)

    loaded = memory.load()
    assert loaded == messages

def test_load_with_limit(memory_path):
    memory = JsonlMemory(memory_path)
    for i in range(10):
        memory.append(Message(role="user", content=f"msg {i}"))

    loaded = memory.load(limit=3)
    assert len(loaded) == 3
    assert loaded[0].content == "msg 7"
    assert loaded[-1].content == "msg 9"

def test_load_more_than_available(memory_path):
    memory = JsonlMemory(memory_path)
    for i in range(5):
        memory.append(Message(role="user", content=f"msg {i}"))

    loaded = memory.load(limit=10)
    assert len(loaded) == 5
    assert loaded[0].content == "msg 0"
    assert loaded[-1].content == "msg 4"

def test_load_with_malformed_lines(memory_path):
    with memory_path.open("w", encoding="utf-8") as f:
        f.write(json.dumps({"role": "user", "content": "valid"}) + "\n")
        f.write("invalid json\n")
        f.write(json.dumps({"role": "assistant", "content": "also valid"}) + "\n")

    memory = JsonlMemory(memory_path)
    loaded = memory.load()
    assert len(loaded) == 2
    assert loaded[0].content == "valid"
    assert loaded[1].content == "also valid"

def test_load_large_messages(memory_path):
    memory = JsonlMemory(memory_path)
    large_content = "x" * 10000
    memory.append(Message(role="user", content="small"))
    memory.append(Message(role="assistant", content=large_content))

    loaded = memory.load()
    assert len(loaded) == 2
    assert loaded[1].content == large_content

def test_load_exact_chunk_boundary(memory_path):
    # chunk_size is 4096. Let's create messages that sum up to exactly something interesting.
    memory = JsonlMemory(memory_path)
    # Each message will be ~1000 bytes
    for i in range(10):
        memory.append(Message(role="user", content="x" * 1000))

    loaded = memory.load(limit=5)
    assert len(loaded) == 5
