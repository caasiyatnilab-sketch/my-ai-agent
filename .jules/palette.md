## 2025-05-15 - Misleading error messages from overloaded exception types
**Learning:** In Python, catching `ValueError` to detect path traversal can accidentally swallow `UnicodeDecodeError` (which inherits from `ValueError`), leading to misleading UX where a binary file is reported as "outside the workspace".
**Action:** Always isolate path validation logic from file reading logic, or catch specific exceptions as close to the source as possible to ensure accurate error feedback.
