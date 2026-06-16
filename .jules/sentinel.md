## 2025-05-15 - Resource Exhaustion Protection in AI Agent Components
**Vulnerability:** Multiple components were susceptible to resource exhaustion:
1. `Calculator` tool: CPU/memory exhaustion via large exponents and result magnitudes.
2. `WorkspaceReader` tool: OOM risk by reading entire files into memory before slicing.
3. `JsonlMemory`: OOM risk by reading the entire conversation history file into memory.

**Learning:** Resource exhaustion (DoS) is a common vulnerability in AI agents that handle untrusted input or unbounded local state. Standard library methods like `read_text()` or `splitlines()` on file contents are often unsafe for files that can grow indefinitely or are controlled by external factors.

**Prevention:**
- Enforce explicit limits on mathematical operations (exponent size and result magnitude).
- Use bounded reads (`f.read(max_chars)`) for file system tools.
- Implement chunked reverse-file reading for loading the tail of log/history files to keep memory usage constant regardless of file size.
