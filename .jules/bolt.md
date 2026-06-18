## 2025-05-15 - Memory Loading Performance
**Learning:** Loading JSONL history by reading the entire file and splitting lines is O(N) where N is the total history size. For long-running agents, this causes linear degradation of every request. Using a chunked reverse-read strategy with `f.seek` allows O(1) loading (relative to file size) of the last `limit` messages.
**Action:** Always prefer reverse-file reading for append-only logs or history when only the most recent entries are needed.
