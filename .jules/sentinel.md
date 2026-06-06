## 2025-05-14 - Resource Exhaustion in Tools
**Vulnerability:** The `Calculator` tool was susceptible to CPU/memory exhaustion via large exponents (e.g., `10**10**10`), and `WorkspaceReader` could cause OOM by reading large files entirely into memory.
**Learning:** Even with a restricted AST subset, certain operators like `ast.Pow` can still trigger resource exhaustion. Similarly, `path.read_text()` is unsafe for potentially large files in a workspace.
**Prevention:** Always impose limits on mathematical operations (like exponent size) and use streaming reads for file system access in agent tools.
