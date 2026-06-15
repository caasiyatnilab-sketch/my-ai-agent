## 2025-05-15 - Explicit Truncation Warning in CLI
**Learning:** For CLI tools that read and display file content, silent truncation can be confusing as users might assume they are seeing the full file. Adding a clear, explicit warning about truncation improves the user's mental model of the tool's state.
**Action:** Always provide visual or textual feedback when output is programmatically limited or truncated.
