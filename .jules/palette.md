## 2025-05-15 - Explicit Truncation Warning
**Learning:** For command-line or text-based tools with output limits, implicit truncation causes confusion and data loss awareness issues. Providing a clear, bracketed warning `[TRUNCATED: Only the first N characters are shown]` ensures the user (or another agent) knows the context is incomplete.
**Action:** Always append a clear truncation notice when trimming long text outputs in file-reading or logging tools.
