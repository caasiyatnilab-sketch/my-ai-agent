## 2025-06-09 - Explicit Truncation Warning
**Learning:** Silent truncation of large file outputs in CLI tools can lead to user confusion and AI hallucinations. Providing a clear, bracketed warning ensures both humans and agents are aware they are looking at partial data.
**Action:** Always append a truncation notice when limiting the output of file-reading or data-fetching tools.
