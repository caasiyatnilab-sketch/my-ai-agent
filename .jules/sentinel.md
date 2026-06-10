## 2025-05-14 - Calculator Denial of Service
**Vulnerability:** The `Calculator` tool was susceptible to CPU and memory exhaustion via extremely large mathematical expressions (e.g., `2**100**100`).
**Learning:** Using `ast.parse` protects against code execution, but doesn't inherently prevent resource exhaustion from valid arithmetic operations that produce massive numbers or take long to compute.
**Prevention:** Implement explicit limits on exponents and result magnitude within the AST evaluation logic.

## 2025-05-14 - OpenAI Compatibility Pattern
**Vulnerability:** Functional incompatibility with OpenAI API when using custom "tool" roles without proper tool call IDs.
**Learning:** The standard OpenAI-compatible provider implementation does not support messages with the 'tool' role without a corresponding `tool_call_id`.
**Prevention:** Concatenate tool outputs into the user message content to ensure compatibility and prevent API errors.
