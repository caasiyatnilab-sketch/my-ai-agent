## 2024-06-27 - Resource Exhaustion in Safe Calculator and WorkspaceReader
**Vulnerability:** Denial of Service (DoS) and Memory Exhaustion (OOM) via unbounded arithmetic operations and large file reads in tool implementations.
**Learning:** Even when using `ast.parse` and a safe subset of operations, Python's arbitrary-precision integers and power operations can still lead to CPU/memory exhaustion. Similarly, `Path.read_text()` loads the entire file into memory, which is risky for an AI agent that might be directed to read large files or pipes.
**Prevention:** Always enforce strict resource limits (exponent size, result magnitude, bit length) on untrusted arithmetic expressions and use iterative reading (`f.read(max_chars)`) for file operations.
