# Palette's UX Journal

## 2025-05-22 - Explicit Truncation Warning
**Learning:** In CLI tools, silent truncation of large file content can lead to user confusion and LLM hallucinations as they are unaware of the missing context.
**Action:** Always append a clear, bracketed warning when content is truncated to ensure all actors know they are seeing a partial view.
