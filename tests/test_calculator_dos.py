import pytest
from my_ai_agent.tools import Calculator

def test_calculator_dos_protection_exponent():
    calc = Calculator()
    # Exponent just within limit
    # 2**300 is approx 2e90, which is < 1e100
    result = calc.run("2**300")
    assert result.ok is True

    # Exponent outside limit
    result = calc.run("2**1001")
    assert result.ok is False
    assert "exponent too large" in result.output

def test_calculator_dos_protection_multiplication():
    calc = Calculator()
    # Large multiplication within limit
    # 10**50 * 10**40 = 10**90 < 1e100
    result = calc.run("10**50 * 10**40")
    assert result.ok is True

    # Large multiplication outside result magnitude limit
    result = calc.run("(10**1000) * (10**1000)")
    assert result.ok is False
    assert "result too large" in result.output

    # Large multiplication outside bit length limit (but within result magnitude)
    # 10**100 is about 333 bits.
    # (10**1000) * (10**1000) was already caught by result too large.
    # To catch bit_length specifically, we'd need bit_length > 10000 but result < 1e100.
    # log2(10**100) is ~332.
    # We'd need something with many bits but small value? Not possible for positive integers.
    # But wait, bit_length() + bit_length() > 10000
    # 2**5000 has bit_length 5001.
    # 2**5000 * 2**5001 has bit_length sum 10002.
    # Value is 2**10001, which is definitely > 1e100.
    # So "result too large" will usually catch it first if it's 1e100.

def test_calculator_dos_protection_result_magnitude():
    calc = Calculator()
    # Result just within magnitude limit (1e100)
    result = calc.run("10**100")
    assert result.ok is True

    # Result outside magnitude limit
    result = calc.run("10**101")
    assert result.ok is False
    assert "result too large" in result.output

def test_calculator_dos_protection_float_magnitude():
    calc = Calculator()
    # Float result outside magnitude limit
    result = calc.run("1e101")
    assert result.ok is False
    assert "result too large" in result.output
