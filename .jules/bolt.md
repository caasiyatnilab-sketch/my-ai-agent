## 2025-05-15 - Reverse JSONL loading for memory
**Learning:** Loading entire JSONL files to retrieve the last few messages is an $O(N)$ operation that scales poorly as conversation history grows. Using chunked reverse-file reading converts this to $O(K)$ where $K$ is the number of messages requested.
**Action:** Always prefer backward-reading for append-only logs or history files when only the most recent entries are needed. Use `f.seek(0, os.SEEK_END)` and read chunks backwards while managing line reconstruction.
