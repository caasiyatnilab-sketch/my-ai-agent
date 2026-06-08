## 2025-05-15 - [Resource Exhaustion via Mathematical Expressions]
**Vulnerability:** A Denial of Service (DoS) vulnerability was identified in the `Calculator` tool where extremely large exponents (e.g., `10**10**10`) could cause CPU exhaustion.
**Learning:** Simple exponent limits on `ast.Pow` (e.g., checking if the exponent > 1000) can be bypassed by nested power expressions (e.g., `(a**b)**c`) if the intermediate results are not also validated. However, a simple exponent limit on any `ast.Pow` node is a good first line of defense.
**Prevention:** Always implement exponent limits in mathematical evaluations and use limited reads (e.g., `f.read(max_chars)`) for file system tools to prevent resource exhaustion.
