## 2026-06-21 - [Calculator Resource Exhaustion DoS]
**Vulnerability:** The Calculator tool allowed unbounded exponents in power operations and unbounded result magnitudes, leading to CPU and memory exhaustion (DoS) during evaluation and string conversion.
**Learning:** Python's ast.parse is safe against code execution but not against resource exhaustion. Default integer-to-string conversion limits provide some protection but can be bypassed or cause unhandled ValueErrors.
**Prevention:** Explicitly limit mathematical operation parameters (like exponents) and result magnitudes before they reach dangerous levels.
