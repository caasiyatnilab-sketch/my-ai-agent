## 2025-05-15 - Calculator DoS via Large Exponents
**Vulnerability:** The `Calculator` tool allowed arbitrary exponentiation, which could lead to CPU exhaustion (e.g., `9**9**9`) or memory exhaustion/`ValueError` when converting huge results to strings.
**Learning:** Even when using `ast.parse` and a whitelist of operators, mathematical operations themselves can be used for Denial of Service if not bounded.
**Prevention:** Always implement limits on exponent size and total result magnitude when evaluating user-provided mathematical expressions.
