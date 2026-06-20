## 2025-05-15 - CLI "Thinking..." indicator and output spacing
**Learning:** Users perceive long-running CLI operations as 'hung' without immediate visual feedback. Adding a transient "Thinking..." indicator and proper spacing between tool results and the final answer significantly improves the perceived responsiveness and scannability of the CLI.
**Action:** Always check if `sys.stdout.isatty()` before writing transient indicators to avoid polluting redirected output or non-interactive logs. Ensure that clearing sequences fully overwrite the indicator.
