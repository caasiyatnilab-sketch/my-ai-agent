## 2025-05-15 - O(N) Memory Loading Bottleneck
**Learning:** `JsonlMemory.load` reads the entire JSONL file into memory using `read_text().splitlines()` before slicing. This causes linear performance degradation as conversation history grows, leading to high memory usage and latency in the `ask` command.
**Action:** Use backward file seeking (`f.seek`) to read only the required number of lines from the end of the file, ensuring O(1) performance relative to file size for loading the latest messages.
