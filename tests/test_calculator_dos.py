import pytest
from my_ai_agent.tools import Calculator

def test_calculator_pow_dos():
    calc = Calculator()
    # This should be caught by our new limits
    result = calc.run("10**10**10")
    assert not result.ok
    assert "exponent too large" in result.output.lower()

def test_calculator_mult_dos():
    calc = Calculator()
    # Large multiplication that could consume CPU/memory
    # Use powers to create large integers without hitting int-to-string parsing limit
    expr = "(10**1000) * (10**1000) * (10**1000) * (10**1000)"
    result = calc.run(expr)
    assert not result.ok
    # It might hit result too large first if we are not careful,
    # but (10**1000) has bit length ~3322.
    # 3322 * 4 = 13288 > 10000.
    assert any(msg in result.output.lower() for msg in ["multiplication result too large", "result too large"])

def test_calculator_result_magnitude_dos():
    calc = Calculator()
    # Result exceeding 1e100
    result = calc.run("10**101")
    assert not result.ok
    assert "result too large" in result.output.lower()
