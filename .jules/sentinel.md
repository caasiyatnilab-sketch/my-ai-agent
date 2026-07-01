## 2026-07-01 - Calculator DoS Protection
**Vulnerability:** Denial of Service (DoS) via resource-intensive arithmetic operations in the `Calculator` tool.
**Learning:** Even "safe" AST-based evaluation can be vulnerable to resource exhaustion if operations like exponentiation (`**`) or large multiplications are not bounded. Python's `int_max_str_digits` limit (default 4300) only protects against conversion to string, not the actual computation which can still hang the process or consume excessive memory.
**Prevention:** Enforce strict limits on exponents and the bit-length of intermediate integer results, as well as magnitude limits for floats, within the evaluation logic.
