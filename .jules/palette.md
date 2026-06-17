## 2025-05-15 - Visual feedback for CLI latency
**Learning:** Users can perceive long-running CLI operations (like LLM calls) as "hung" if there is no immediate visual feedback. A simple "Thinking..." indicator that disappears once the response arrives improves the perceived responsiveness of the interface.
**Action:** Use `sys.stdout.write('\rThinking...')` with TTY detection and a `finally` block to ensure the indicator is always cleared, preventing it from interfering with the final output.
