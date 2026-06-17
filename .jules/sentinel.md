## 2025-05-15 - Calculator Resource Exhaustion (DoS)
**Vulnerability:** The `Calculator` tool was vulnerable to Denial of Service (DoS) through resource exhaustion. An attacker (or a malfunctioning agent) could provide expressions like `2**100000000` which consume excessive CPU and memory, potentially hanging the process.
**Learning:** Even with a safe subset of `ast`, mathematical operations like exponentiation can still lead to resource exhaustion. Python's default integer string conversion limit (4300 digits) provides some protection but doesn't prevent the calculation itself.
**Prevention:** Implement explicit limits on exponents and the absolute magnitude of results. For `ast.Pow`, cap the exponent at a reasonable value (e.g., 1000). Also, check the magnitude of the result to prevent large memory allocations for huge integers or floats.

## 2025-05-15 - OpenAI Provider Role Compatibility
**Vulnerability:** The agent was using the `tool` role in conversation history, which is not supported by the basic OpenAI-compatible chat completions implementation in this repo and would cause a 400 error from the API.
**Learning:** The `OpenAICompatibleProvider` implementation in this repository does not support the official tool-calling API and thus lacks support for the `tool` message role.
**Prevention:** Concatenate tool results into the `user` message content when using providers that do not support the `tool` role.
