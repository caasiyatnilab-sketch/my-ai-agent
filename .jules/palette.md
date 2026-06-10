## 2025-05-14 - [Explicit Truncation Warnings]
**Learning:** For CLI tools that limit output (e.g., file readers), silent truncation can confuse users who might assume they received the full content. Adding a clear, bracketed warning at the end of the output provides immediate clarity and avoids misinterpretation of data.
**Action:** Always include a visual indicator or warning when programmatically truncating output in CLI interfaces.
