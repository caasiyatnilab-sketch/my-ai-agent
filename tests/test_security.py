from my_ai_agent.tools import Calculator


def test_calculator_large_exponent():
    calc = Calculator()
    # Large exponent should be rejected
    result = calc.run("2**1000001")
    assert not result.ok
    assert "exponent" in result.output.lower() or "too large" in result.output.lower()


def test_calculator_large_result_magnitude():
    calc = Calculator()
    # Large result magnitude should be rejected even if individual exponents are small
    # (10**60)**2 = 10**120
    result = calc.run("(10**60)**2")
    assert not result.ok
    assert "too large" in result.output.lower() or "magnitude" in result.output.lower()


def test_agent_memory_compatibility():
    import tempfile
    from pathlib import Path

    from my_ai_agent.agent import Agent
    from my_ai_agent.config import AgentConfig
    from my_ai_agent.providers import MockProvider

    with tempfile.TemporaryDirectory() as tmpdir:
        mem_path = Path(tmpdir) / "memory.jsonl"
        config = AgentConfig(openai_api_key="test", memory_path=mem_path)
        agent = Agent(config=config, provider=MockProvider())

        # Trigger a tool run
        agent.ask("calc: 2+2")

        # Verify memory contains no 'tool' role
        messages = agent.memory.load()
        for msg in messages:
            assert msg.role != "tool", "OpenAI provider does not support 'tool' role"
