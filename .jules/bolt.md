## 2025-05-15 - Optimizing JSONL Loading with Binary Backward Seeking

**Learning:** Loading the entire conversation history into memory to retrieve only the last few messages is a significant performance bottleneck as the history file grows. Using binary backward seeking allows O(1) or O(limit) access to the end of the file regardless of its total size.

**Action:** For append-only log files or history files where only the most recent entries are needed, always prefer backward seeking over reading the whole file. Use `f.seek(0, os.SEEK_END)` and read in chunks from the end.
