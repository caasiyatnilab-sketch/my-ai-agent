## 2025-05-14 - Resource Exhaustion in AST-based Calculator
**Vulnerability:** The AST-based calculator was vulnerable to CPU and memory exhaustion (DoS) via extremely large exponents (e.g., `10**10**10`) and massive result magnitudes.
**Learning:** Even a restricted AST evaluator is not safe from resource exhaustion if mathematical operations can produce numbers that exceed computational limits or memory. Simple exponent checks on `ast.Pow` can be bypassed by nesting operations (e.g., `(10**100)**2`) if intermediate results aren't also validated.
**Prevention:** Always implement hard limits on exponents for power operations AND validate the absolute magnitude of all results (intermediate and final) against a reasonable threshold (e.g., 1e100).
