## 2025-05-15 - Resource Exhaustion in Tools and Memory
**Vulnerability:** Denial of Service (DoS) via CPU exhaustion (Calculator) and Memory exhaustion (WorkspaceReader, JsonlMemory).
**Learning:** Evaluated Python code (even in a "safe" subset) can be abused to consume excessive CPU or memory if numeric operations aren't bounded. Similarly, file reading operations that load entire files into memory are high-risk for OOM.
**Prevention:** Always enforce strict bounds on resource-intensive operations:
1. Bound exponents in `ast.Pow`.
2. Bound bit-length in multiplications.
3. Bound absolute magnitude of arithmetic results.
4. Use iterative/partial reading for files instead of loading them entirely.
5. Use binary backward seeking for tail-loading log/history files.
