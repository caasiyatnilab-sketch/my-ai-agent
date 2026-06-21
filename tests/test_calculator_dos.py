from my_ai_agent.tools import Calculator


def test_calculator_dos_exponent():
    calc = Calculator()
    result = calc.run("2**1001")
    assert result.ok is False
    assert "Exponent too large" in result.output


def test_calculator_dos_magnitude():
    calc = Calculator()
    result = calc.run("10**101")
    assert result.ok is False
    assert "Result too large" in result.output


def test_calculator_safe_exponent():
    calc = Calculator()
    result = calc.run("2**10")
    assert result.ok is True
    assert result.output == "1024"


def test_calculator_negative_exponent_safe():
    calc = Calculator()
    # 2**-1 is 0.5, which is safe
    result = calc.run("2**-1")
    assert result.ok is True
    assert result.output == "0.5"


def test_calculator_large_negative_exponent_safe_magnitude():
    calc = Calculator()
    # 0.1**1000 is very small but absolute magnitude is < 1e100 (it's 1e-1000)
    # Wait, abs(1e-1000) is 1e-1000 which IS less than 1e100.
    # However, 0.1**1000 should be fine.
    result = calc.run("0.1**1000")
    assert result.ok is True


def test_calculator_large_result_addition():
    calc = Calculator()
    result = calc.run("1e100 + 1e100")
    assert result.ok is False
    assert "Result too large" in result.output
