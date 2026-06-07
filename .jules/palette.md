## 2025-05-14 - Explicit Truncation Feedback
**Learning:** For CLI tools that truncate long text output (e.g., WorkspaceReader), appending a clear, bracketed warning informs the user and ensures the agent receives the correct context about the incomplete data.
**Action:** Always append a `[TRUNCATED: ...]` message when limiting string output in tools to maintain transparency.
