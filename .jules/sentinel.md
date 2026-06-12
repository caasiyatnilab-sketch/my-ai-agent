## 2024-06-12 - Calculator Resource Exhaustion (DoS) Protection
**Vulnerability:** The `Calculator` tool was susceptible to Denial of Service (DoS) via resource exhaustion. Specifically, extremely large exponents in `ast.Pow` or operations resulting in massive integers could hang the process or consume excessive memory.
**Learning:** Simple exponent limits on `ast.Pow` (e.g., checking if the exponent > 1000) can be bypassed by nested power expressions (e.g., `(a**b)**c`) if the intermediate results or the final result magnitude are not also validated.
**Prevention:** Implement both exponent limits for `ast.Pow` AND absolute magnitude limits for all arithmetic results.

## 2024-06-12 - Memory-Safe File Reading
**Vulnerability:** `WorkspaceReader` used `Path.read_text()` followed by slicing, which reads the entire file into memory before truncating. This is a potential memory-based DoS (OOM) for very large files.
**Learning:** For tools that expose file system access, always use bounded reads (e.g., `file.read(max_chars)`) instead of reading the full content into memory.
**Prevention:** Use `with open(...) as f: f.read(limit)` to ensure only the requested amount of data is ever loaded.
