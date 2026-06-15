## 2025-05-14 - Resource Exhaustion in Tooling
**Vulnerability:** The `Calculator` tool was susceptible to CPU exhaustion (DoS) via large exponents (e.g., `10**10**10`), and `WorkspaceReader` could cause OOM by reading very large files into memory before truncating.
**Learning:** Even "safe" AST-based evaluation can be abused if result magnitudes and operations are not bounded. Standard library `read_text()` is not suitable for untrusted file sizes if a character limit is intended.
**Prevention:** Always implement exponent limits in mathematical evaluations and use limited reads (`f.read(max_chars)`) for file system tools.

## 2025-05-14 - Memory and Provider OOM Risks
**Vulnerability:** `JsonlMemory.load` used `read_text()` on potentially large history files, and `OpenAICompatibleProvider` used `response.read()` without limits on API responses.
**Learning:** Historical data and external API responses can grow beyond expected bounds, leading to memory exhaustion if read in their entirety.
**Prevention:** Use chunked reverse-reading for history files and enforce strict byte limits on API response consumption.
