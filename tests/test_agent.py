from pathlib import Path

from my_ai_agent import Agent, AgentConfig


def make_agent(tmp_path: Path) -> Agent:
    config = AgentConfig(memory_path=tmp_path / "memory.jsonl", workspace=tmp_path)
    return Agent(config)


def test_ask_works_offline_and_persists_memory(tmp_path: Path) -> None:
    agent = make_agent(tmp_path)

    result = agent.ask("hello", use_memory=False)

    assert "Mock response" in result.answer
    assert (tmp_path / "memory.jsonl").read_text(encoding="utf-8").count("\n") == 2


def test_inline_calculator_tool(tmp_path: Path) -> None:
    agent = make_agent(tmp_path)

    result = agent.ask("calc: 2 * (3 + 4)", use_memory=False)

    assert result.tool_results[0].ok is True
    assert result.tool_results[0].output == "14"


def test_calculator_rejects_unsafe_code(tmp_path: Path) -> None:
    agent = make_agent(tmp_path)

    result = agent.calculate("__import__('os').system('echo nope')")

    assert result.ok is False
    assert "Unsupported syntax" in result.output


def test_calculator_rejects_large_exponent(tmp_path: Path) -> None:
    agent = make_agent(tmp_path)

    result = agent.calculate("2**1001")

    assert result.ok is False
    assert "Exponent too large" in result.output


def test_calculator_rejects_large_result(tmp_path: Path) -> None:
    agent = make_agent(tmp_path)

    result = agent.calculate("10**101")

    assert result.ok is False
    assert "Calculation result too large" in result.output


def test_workspace_reader_blocks_path_traversal(tmp_path: Path) -> None:
    agent = make_agent(tmp_path)

    result = agent.read_file("../secret.txt")

    assert result.ok is False
    assert "outside" in result.output


def test_workspace_reader_reads_workspace_file(tmp_path: Path) -> None:
    (tmp_path / "note.txt").write_text("important", encoding="utf-8")
    agent = make_agent(tmp_path)

    result = agent.read_file("note.txt")

    assert result.ok is True
    assert result.output == "important"
