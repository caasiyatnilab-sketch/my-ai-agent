## 2025-05-15 - Optimized JSONL memory loading with reverse file reading
**Learning:** Reading large JSONL files from the beginning and splitting them into lines is $O(n)$ in both time and memory. For conversation histories that only need the last $N$ messages, this becomes a significant bottleneck as history grows.
**Action:** Use chunked reverse binary reading with `seek()` to fetch only the required trailing lines. Ensure safe UTF-8 decoding by splitting at the `0x0A` (newline) byte, which is a stable delimiter in UTF-8.
