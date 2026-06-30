# Palette's Journal

## 2025-06-21 - Thinking Indicator for CLI
**Learning:** Users perceive long-running CLI operations (like LLM calls) as 'hung' without immediate visual feedback. A transient 'Thinking...' indicator improves perceived responsiveness.
**Action:** Use `sys.stderr.write('\rThinking...')` followed by a flush and a subsequent clearing sequence (e.g., '\r' + 12 spaces + '\r') in a `finally` block to provide non-intrusive visual feedback during long-running CLI operations in interactive terminals.
