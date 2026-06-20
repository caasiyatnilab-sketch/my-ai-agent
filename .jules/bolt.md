## 2025-05-15 - Seek-based tail read for large history files
**Learning:** Loading conversation history by reading the entire JSONL file and using `splitlines()[-limit:]` is O(N) where N is the file size. For long-running agents, this becomes a significant bottleneck. Using `f.seek(0, os.SEEK_END)` and reading backwards in chunks provides O(limit) performance.
**Action:** Always prefer seek-based tail reads when only the last few entries of a large append-only log or history file are needed.
