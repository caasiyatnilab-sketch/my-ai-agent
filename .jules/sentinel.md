## 2025-05-22 - Calculator DoS via Resource Exhaustion
**Vulnerability:** The Calculator tool allowed arbitrary arithmetic expressions, which could lead to Denial of Service via CPU/memory exhaustion (e.g., very large exponents or massive intermediate results).
**Learning:** Even with safe AST-based evaluation (avoiding `eval()`), mathematical operations like exponentiation can still be used to crash a process or consume excessive resources if operands and results are not bounded.
**Prevention:** Explicitly limit the exponent in power operations (e.g., max 1000) and check the absolute magnitude of all intermediate and final results (e.g., max 1e100).
