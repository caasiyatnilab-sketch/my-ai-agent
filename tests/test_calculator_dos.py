from my_ai_agent.tools import Calculator

def test_calculator_dos_protection():
    calc = Calculator()
    # Exponent limit
    assert "Exponent too large" in calc.run("10**1001").output
    # Multiplication bit-length limit
    assert "Multiplication result too large" in calc.run(f"{2**5000} * {2**5000}").output
    # Result magnitude limit
    assert "Result too large" in calc.run("10**101").output
    # Safe ops still work
    assert calc.run("2 + 2").output == "4"
