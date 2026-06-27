import pytest
from pathlib import Path
from my_ai_agent.tools import Calculator, WorkspaceReader

def test_calculator_exponent_limit():
    calc = Calculator()
    result = calc.run("10**1001")
    assert not result.ok
    assert "exponent too large" in result.output

def test_calculator_magnitude_limit():
    calc = Calculator()
    # 10**100 should be ok (it's exactly 1e100)
    # Wait, my check was `abs(result) > 1e100`
    result = calc.run("10**100")
    assert result.ok

    result = calc.run("10**101")
    assert not result.ok
    assert "result too large" in result.output

def test_calculator_multiplication_limit():
    calc = Calculator()
    # (10**1000) * (10**1000) should be blocked by multiplication bit length check
    # 10**1000 is ~3322 bits. 3322 + 3322 = 6644, which is < 10000.
    # Let's use something larger.
    # 10**2000 is ~6644 bits. 6644 + 6644 = 13288, which is > 10000.
    # But wait, 10**2000 will be blocked by exponent limit 1000.

    # Let's try (10**1000) * (10**1000) * (10**1000) * (10**1000)
    # Actually, the check is on each BinOp.
    # So if we have (10**1000) * (10**1000), it's 3322 + 3322 = 6644 bits.
    # If we then do that * (10**1000), it's 6644 + 3322 = 9966 bits.
    # * (10**1000) again -> 9966 + 3322 = 13288 bits.

    # (2**5000) * (2**5001) = 2**10001, which is > 10000 bits.
    # Magnitude check comes after. 2**5000 is huge, so it will hit magnitude check first IF we don't have it blocked.
    # Wait, magnitude check is > 1e100. 1e100 is ~333 bits.
    # So most things hitting the bit limit will also hit the magnitude limit.

    # Let's use negative numbers to stay small in magnitude? No, absolute magnitude.
    # Bit length check is for integers.

    # If I want to hit bit length check but NOT magnitude check, it's impossible
    # because bit length check is 10000 bits (~3000 digits)
    # and magnitude limit is 1e100 (100 digits).

    # Magnitude check (1e100) is much stricter than bit length check (10000 bits).
    # Most things will hit magnitude check first.
    expr = "10**60 * 10**60"
    result = calc.run(expr)
    assert not result.ok
    assert "result too large" in result.output

def test_workspacereader_memory_efficiency(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    large_file = workspace / "large.txt"
    content = "A" * 10000
    large_file.write_text(content, encoding="utf-8")

    reader = WorkspaceReader(workspace)
    result = reader.run("large.txt", max_chars=10)
    assert result.ok
    assert result.output == "A" * 10
    assert len(result.output) == 10

def test_workspacereader_unicode_decode_error(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    binary_file = workspace / "binary.bin"
    binary_file.write_bytes(b"\xff\xfe\xfd") # Invalid UTF-8

    reader = WorkspaceReader(workspace)
    result = reader.run("binary.bin")
    assert not result.ok
    assert "Could not read file" in result.output
