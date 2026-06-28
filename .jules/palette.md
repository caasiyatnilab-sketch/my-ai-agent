## 2025-05-15 - Improving WorkspaceReader feedback
**Learning:** Broad exception catching like `except ValueError` can swallow more specific errors like `UnicodeDecodeError`, leading to confusing UX (e.g. reporting a binary file as "outside workspace").
**Action:** Always handle specialized exceptions (like `UnicodeDecodeError`) before more general ones, and provide specific, actionable feedback to the user.
