## 2024-06-30 - Resource Exhaustion in Agent Tools
**Vulnerability:** DoS and OOM via unbound arithmetic operations and file reads in tools.
**Learning:** Even "safe" subsets of languages (like `ast.eval`) can be abused for resource exhaustion if operations like `**` or large file reads are not restricted.
**Prevention:** Implement strict limits on exponents, result magnitudes, and use iterative reading for file access.
