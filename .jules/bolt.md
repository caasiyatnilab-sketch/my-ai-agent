## 2026-06-15 - Optimize JSONL memory loading with reverse-read
**Learning:** For append-only files where only the most recent entries are needed, reading the entire file (O(n)) is a massive bottleneck. A chunked reverse-read strategy using binary mode and `seek` can provide >1000x speedups for large files.
**Action:** Use `f.seek(0, 2)` to start from the end and read backwards in chunks when implementing pagination or fetching recent history from logs or JSONL files.
