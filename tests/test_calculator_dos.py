import pytest
from my_ai_agent.tools import Calculator

def test_calculator_dos_protection():
    calc = Calculator()

    # Test exponent limit
    result = calc.run("2**1001")
    assert not result.ok
    assert "exponent too large" in result.output

    # Test logarithmic protection (too large power before it's computed)
    result = calc.run("(2**100)**50")
    assert not result.ok
    assert "result too large" in result.output

    # Test multiplication limit (too large result before it's computed)
    result = calc.run("10**60 * 10**60")
    assert not result.ok
    assert "result too large" in result.output

    # Test safe values
    result = calc.run("2**100")
    assert result.ok

    result = calc.run("10**100")
    assert result.ok

    # Test nested operations that stay within limits
    result = calc.run("(2**5)**10")
    assert result.ok
    assert result.output == str(2**50)
