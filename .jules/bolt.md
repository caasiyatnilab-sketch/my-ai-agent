## 2025-05-15 - Optimizing JSONL loading with backward seek
**Learning:** For append-only log files like conversation history, loading the entire file to get the last N lines is an O(n) operation that scales poorly. Binary backward seeking allows for O(1) tail loading regardless of file size.
**Action:** Always prefer backward seeking or indexing for tail-heavy access patterns in local storage.
