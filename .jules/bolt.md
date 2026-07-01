## 2025-05-15 - Optimize JSONL Loading with Backward Seek
**Learning:** Implementing binary backward seeking in `JsonlMemory.load` provides a massive speedup (~600x for 10MB) for loading tail ends of large conversation history files. This avoids the O(n) memory and CPU cost of reading the entire file.
**Action:** Always prefer partial reads/seeking when only a small portion of a large log or history file is needed.
