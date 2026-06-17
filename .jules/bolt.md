## 2025-05-15 - Optimized memory loading with chunked reverse-read
**Learning:** Loading the entire JSONL history file only to slice the last few lines becomes a significant bottleneck as the file grows. A chunked reverse-reading approach (using binary mode and seeking from the end) provides a massive performance boost.
**Action:** Use chunked reverse-reading for any append-only logs or history files where only the most recent entries are needed.
