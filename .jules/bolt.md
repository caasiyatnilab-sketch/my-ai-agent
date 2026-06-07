## 2025-05-15 - Optimize JSONL memory loading with reverse reading
**Learning:** Reading large JSONL history files in their entirety to extract only the last $N$ lines is an O(n) operation that wastes memory and time. For a 14MB file with 100k messages, this took ~0.06-0.23 seconds.
**Action:** Implement chunked reverse-file reading to fetch only the needed lines. This reduced the load time to <0.001 seconds (effectively O(1) relative to total file size).

## 2025-05-15 - OpenAI Role Compatibility
**Learning:** The OpenAI Chat Completions API requires `tool_call_id` for messages with the `tool` role. Simple inline tool implementations without formal ID generation should store tool outputs within augmented `user` role messages to maintain API compatibility for multi-turn conversations.
**Action:** Persist augmented user messages containing tool results instead of separate tool role messages.
