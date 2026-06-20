## 2025-05-15 - Arithmetic Denial of Service (DoS) in Calculator
**Vulnerability:** The `Calculator` tool was susceptible to CPU and memory exhaustion via extremely large exponents (e.g., `9**9**9`) and massive integer-to-string conversions.
**Learning:** Even if using `ast.parse` for safety, Python's arbitrary-precision integers can still be exploited for resource exhaustion. The default `sys.set_int_max_str_digits` limit (4300) provides some protection but can still cause unexpected `ValueError` crashes.
**Prevention:** Explicitly validate and cap exponents in `ast.Pow` nodes and check the magnitude of results before conversion or further computation.

## 2025-05-15 - Unbounded API Response Consumption
**Vulnerability:** `OpenAICompatibleProvider.complete` was reading the entire response body into memory using `response.read()` without a size limit.
**Learning:** Trusting external or even internal API endpoints to send reasonably sized responses is a risk. Malicious or misconfigured servers can send multi-gigabyte responses leading to Out-of-Memory (OOM) conditions.
**Prevention:** Always use a size limit when reading from network streams (e.g., `response.read(MAX_SIZE)`).
