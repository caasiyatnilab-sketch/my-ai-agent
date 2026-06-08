## 2026-06-08 - Explicit Truncation Feedback
**Learning:** When a tool silently truncates output to prevent resource exhaustion, both the human user and the AI agent may lose critical context without knowing why. Providing an explicit, visible truncation notice in the UI/output ensures the user is aware of the limitation and can take corrective action (like reading specific parts of a file).
**Action:** Always append clear metadata or warnings when output is programmatically limited or filtered.
