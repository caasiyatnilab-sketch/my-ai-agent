## 2026-06-05 - [Efficient file reading for bounded reads]
**Learning:** Using `pathlib.Path.read_text()` followed by slicing is highly inefficient for large files as it loads the entire content into memory. For bounded reads, using `file.read(N)` is much faster.
**Action:** Prefer `f.read(n)` for bounded file reads.
