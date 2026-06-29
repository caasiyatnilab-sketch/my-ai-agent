# Bolt's Performance Journal

## 2025-05-15 - Binary Backward Seeking for JSONL
**Learning:** Loading large JSONL files by reading the entire content into memory and splitting lines is inefficient (O(n) time and space), especially when only the last few entries are needed. Binary backward seeking allows for O(1) time complexity (relative to file size) to retrieve the tail of a file.
**Action:** Use binary seeking for any append-only logs or memory files where only the most recent N entries are required.
