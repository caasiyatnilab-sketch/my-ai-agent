## 2026-06-21 - [Thinking indicator for CLI]
**Learning:** Users perceive long-running CLI operations (like LLM calls) as 'hung' without immediate visual feedback. A transient 'Thinking...' indicator improves perceived responsiveness.
**Action:** Use `sys.stdout.write('\rThinking...')` followed by a flush and a subsequent clearing sequence (e.g., `\r` + spaces + `\r`) to provide non-intrusive visual feedback during long-running CLI operations.
