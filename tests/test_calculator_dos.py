
from my_ai_agent.tools import Calculator
import pytest

def test_calculator_pow_dos_prevention():
    calc = Calculator()
    # This should be blocked or handled safely after the fix
    result = calc.run("2**1000000000")
    # Before fix, this might crash or raise ValueError (4300 digits limit)
    # After fix, we expect a graceful error message
    assert not result.ok
    assert "exponent too large" in result.output.lower()

def test_calculator_mult_dos_prevention():
    calc = Calculator()
    # Multiplication of very large numbers
    large = "1" + "0" * 2000
    result = calc.run(f"{large} * {large}")
    assert not result.ok
    assert "multiplication result too large" in result.output.lower()

def test_calculator_result_magnitude_limit():
    calc = Calculator()
    # This might result in a very large number that doesn't necessarily have many digits in decimal
    # but still could be problematic
    result = calc.run("10**500")
    assert not result.ok
    assert "too large" in result.output.lower()
