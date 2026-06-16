## 2026-06-16 - Efficient reverse-file reading for JSONL memory
**Learning:** For append-only JSONL files where only the most recent entries are needed, reading the entire file into memory is O(n) in both time and space. Implementing a chunked reverse-read strategy using binary mode and `f.seek(0, os.SEEK_END)` allows for O(limit) performance, where `limit` is the number of lines requested.
**Action:** Use bounded reverse reads when fetching tailing entries from log-like files to prevent OOM risks and improve responsiveness as the file grows.
