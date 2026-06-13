## 2026-06-13 - Multi-Layer DoS Protection in Python Tools
**Vulnerability:** Resource exhaustion (DoS) via mathematical operations, large file reads, and unbounded memory loading of history.
**Learning:** Simple exponent limits on `ast.Pow` can be bypassed or still lead to massive numbers if the base is large; magnitude checks on results are necessary. Additionally, standard library `Path.read_text().splitlines()` is a DoS vector for files that grow over time (like logs or memory).
**Prevention:** Implement magnitude checks (e.g., `abs(result) > 1e100`) in math tools, use bounded reads (`f.read(max_chars)`) for files, and implement chunked reverse-file reading for fetching the tail of growing history files.
