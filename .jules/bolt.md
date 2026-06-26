## 2026-06-26 - Binary backward seeking for JSONL memory
**Learning:** Reading large history files entirely into memory to get the last few lines is a major performance and memory bottleneck. Binary backward seeking with chunked reading provides a ~1200x speedup for 10MB files.
**Action:** Use binary seeking for any task involving reading the tail of large log or data files.
