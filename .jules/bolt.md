## 2025-05-15 - Optimized memory loading with chunked reverse read
**Learning:** Loading JSONL history by reading the entire file into memory is O(n) and becomes a significant bottleneck as the history grows. For a 100k line file, it took ~0.05s, which is noticeable in a CLI context.
**Action:** Use chunked reverse-file reading to fetch only the required last N lines. This provides a >200x speedup (~0.0002s) and constant memory usage regardless of file size.
