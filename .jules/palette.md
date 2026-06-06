## 2025-05-14 - Truncation clarity in CLI tools
**Learning:** When a CLI tool silently truncates output (like a file reader with a character limit), users (and LLM agents) may be unaware they are viewing incomplete data. This can lead to confusion or incorrect conclusions.
**Action:** Always append a clear, visible warning message (e.g., `[TRUNCATED: ...]`) when output is capped by a limit.
