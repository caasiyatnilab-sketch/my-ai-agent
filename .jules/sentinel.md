## 2025-05-15 - Calculator DoS Protection
**Vulnerability:** Denial of Service (DoS) via resource exhaustion in arithmetic evaluation.
**Learning:** Python's `ast` evaluation and large integer operations can lead to CPU and memory exhaustion (e.g., `10**10**10` or massive multiplications) if not explicitly bounded.
**Prevention:** Implement limits on exponents, multiplication operand bit-lengths, and overall result magnitudes within safe evaluation wrappers.
