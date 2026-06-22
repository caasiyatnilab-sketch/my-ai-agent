## 2026-06-22 - Optimized JSONL Memory Loading
**Learning:** Loading conversation history by reading the entire file into memory (O(N)) becomes a major bottleneck as the history grows. For append-only JSONL files, seeking to the end and reading backward (O(1)) is significantly more efficient for retrieving the most recent messages.
**Action:** Use backward file seeking with `f.seek(0, 2)` and read in chunks for any append-only log-like data structures where only the tail is needed.
