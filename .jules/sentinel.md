# Sentinel Security Journal

## 2025-05-22 - Initial Journal Setup
**Vulnerability:** N/A
**Learning:** Initializing the Sentinel security journal to track critical security learnings and vulnerability patterns specific to this codebase.
**Prevention:** N/A

## 2025-05-22 - Calculator DoS and File Read OOM
**Vulnerability:** Denial of Service (DoS) via resource-intensive arithmetic and Memory Exhaustion (OOM) via large file reads.
**Learning:** Evaluated arithmetic expressions can lead to DoS if they produce extremely large numbers (e.g., `2**100000000`) or perform quadratic growth multiplications. Similarly, reading entire files into memory before truncation can lead to OOM.
**Prevention:**
- Enforce strict limits on exponents (e.g., max 1000) and combined bit-lengths of multiplication operands.
- Cap the magnitude of results before string conversion (e.g., 1e100).
- Use streamed reads (e.g., `f.read(max_chars)`) instead of loading entire file contents into memory.
