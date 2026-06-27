## 2025-06-27 - Optimized JSONL memory loading with backward seeking
**Learning:** Naive `read_text().splitlines()` on a JSONL history file is an O(N) operation that loads the entire file into memory, which becomes a major bottleneck as conversation history grows. Implementing a backward-seeking read in chunks allows loading the last N messages in O(N_messages) time, regardless of file size.
**Action:** Always consider binary backward seeking when reading the end of large log-like files (JSONL, logs) to ensure performance remains constant as the file grows.
