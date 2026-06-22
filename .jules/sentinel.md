# Sentinel Security Journal

## 2025-05-22 - Resource Exhaustion in Local Tools and Providers
**Vulnerability:** Denial of Service (DoS) and Out-of-Memory (OOM) risks in `Calculator` tool, `JsonlMemory`, and `OpenAICompatibleProvider`.
**Learning:** Even "safe" tools (like an AST-based calculator) can be abused to consume excessive CPU or memory if operand magnitudes are not strictly capped *before* execution. Similarly, reading external provider responses or local history files without bounds or chunking poses significant OOM risks.
**Prevention:**
- In `Calculator`: Enforce limits on exponents, multiplication operand bit-lengths, and final result magnitudes.
- In `JsonlMemory`: Use backward file seeking and chunked reading to load the latest history without loading the entire file into memory.
- In `OpenAICompatibleProvider`: Set a hard limit on the number of bytes read from external API responses.
