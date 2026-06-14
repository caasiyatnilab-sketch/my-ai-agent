## 2026-06-14 - Visual Feedback for CLI operations
**Learning:** For terminal-based applications, providing immediate visual feedback for potentially long-running operations (like LLM requests) prevents the user from assuming the application has hung. Using carriage returns (`\r`) allows for updating or clearing these messages without cluttering the terminal history with intermediate states.
**Action:** Always implement a 'Thinking...' or progress indicator for asynchronous or external service calls in CLI tools, and ensure they are cleaned up correctly after completion.
