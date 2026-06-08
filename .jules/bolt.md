## 2025-05-15 - Optimize memory loading with chunked reverse reading
**Learning:** Reading a large JSONL file into memory just to get the last few lines is a major performance bottleneck (O(N) time and memory). Chunked reverse-file reading provides O(1) memory and near O(1) time performance relative to the total file size.
**Action:** Always prefer chunked reverse reading for append-only logs or history files when only the most recent entries are needed.

## 2025-05-15 - Bounded file reads in WorkspaceReader
**Learning:** `Path.read_text()` loads the entire file content into memory. For tools with a `max_chars` limit, this is extremely inefficient for large files.
**Action:** Use `file.read(max_chars)` to only load what is actually needed, preventing OOM and improving latency.
