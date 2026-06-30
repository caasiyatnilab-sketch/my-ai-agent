## 2024-06-30 - Binary backward seeking for JSONL loading
**Learning:** Loading conversation history by reading the entire JSONL file into memory and splitting lines becomes a major bottleneck as the history grows. Implementing binary backward seeking allows loading only the required trailing lines, providing a ~3000x speedup for large files (e.g., 50MB) and preventing OOM issues.
**Action:** Use backward seeking for any append-only log-like files where only the most recent N entries are needed.
