## 2025-05-15 - Calculator DoS Protection
**Vulnerability:** Resource exhaustion (CPU/Memory) in `Calculator` tool via large arithmetic operations (e.g., `10**1000000`).
**Learning:** Python's `int` and `float` calculations can consume excessive resources before hitting string conversion limits. Pre-calculation checks using logarithms are necessary for complete protection.
**Prevention:** Always validate operand magnitudes and predicted result sizes before performing arithmetic in exposed tools.

## 2025-05-15 - OOM Protection in Memory and Providers
**Vulnerability:** Memory exhaustion (OOM) via reading entire large history files or API responses.
**Learning:** `Path.read_text()` and `response.read()` are unsafe for potentially large external data.
**Prevention:** Use backward file seeking for O(1) memory loading and specify byte limits when reading from network responses.
