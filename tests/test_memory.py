import json
from dataclasses import asdict

from my_ai_agent.memory import JsonlMemory
from my_ai_agent.providers import Message


def test_jsonl_memory_load_empty(tmp_path):
    path = tmp_path / "memory.jsonl"
    memory = JsonlMemory(path)
    assert memory.load() == []


def test_jsonl_memory_append_and_load(tmp_path):
    path = tmp_path / "memory.jsonl"
    memory = JsonlMemory(path)

    msg1 = Message(role="user", content="hello")
    msg2 = Message(role="assistant", content="hi there")

    memory.append(msg1)
    memory.append(msg2)

    loaded = memory.load()
    assert len(loaded) == 2
    assert loaded[0] == msg1
    assert loaded[1] == msg2


def test_jsonl_memory_limit(tmp_path):
    path = tmp_path / "memory.jsonl"
    memory = JsonlMemory(path)

    messages = [Message(role="user", content=f"msg {i}") for i in range(10)]
    for msg in messages:
        memory.append(msg)

    loaded = memory.load(limit=3)
    assert len(loaded) == 3
    assert loaded == messages[-3:]


def test_jsonl_memory_invalid_lines(tmp_path):
    path = tmp_path / "memory.jsonl"
    path.write_text('invalid json\n{"role": "user", "content": "valid"}\n', encoding="utf-8")

    memory = JsonlMemory(path)
    loaded = memory.load()
    assert len(loaded) == 1
    assert loaded[0] == Message(role="user", content="valid")


def test_jsonl_memory_large_file_reverse_read(tmp_path):
    path = tmp_path / "memory.jsonl"
    memory = JsonlMemory(path)

    count = 100
    messages = [Message(role="user", content=f"msg {i}") for i in range(count)]
    with path.open("w", encoding="utf-8") as f:
        for msg in messages:
            f.write(json.dumps(asdict(msg)) + "\n")

    # Test loading with limit smaller than file
    loaded = memory.load(limit=10)
    assert len(loaded) == 10
    assert loaded == messages[-10:]

    # Test loading with limit larger than file
    loaded = memory.load(limit=200)
    assert len(loaded) == count
    assert loaded == messages


def test_jsonl_memory_no_trailing_newline(tmp_path):
    path = tmp_path / "memory.jsonl"
    msg = Message(role="user", content="no newline")
    path.write_text(json.dumps(asdict(msg)), encoding="utf-8")

    memory = JsonlMemory(path)
    loaded = memory.load()
    assert len(loaded) == 1
    assert loaded[0] == msg
