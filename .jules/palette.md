## 2026-06-23 - Improve CLI scannability and truncation feedback
**Learning:** Users perceive long-running or tool-heavy CLI output as cluttered if results and answers are not clearly separated. Additionally, silent truncation of large file reads leads to confusion and potential data loss in downstream LLM processing.
**Action:** Always add a blank line between tool results and the final assistant response in CLI applications. Ensure truncation of data is explicitly communicated to the user with a visible notice.
