## 2025-05-14 - Inefficient JSONL tail loading
**Learning:** `JsonlMemory.load()` was reading the entire memory file into memory and splitting it into lines before taking the slice of the last `limit` messages. For large conversation histories, this causes unnecessary O(n) memory and time overhead where n is the total number of historical messages.
**Action:** Use a chunked reverse-file reading approach to only read the necessary bytes from the end of the file until the requested `limit` of messages is satisfied.
