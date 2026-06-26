## 2025-06-26 - Informative Error Messages and Truncation Indicators
**Learning:** Generic error messages (like "Path is outside workspace") when a tool fails for a different reason (like binary data decoding) lead to user confusion. Providing specific feedback and visual indicators for partial results (like truncation) improves trust and clarity.
**Action:** Always check if a catch-all exception block might be masking specific, informative errors that should be surfaced to the user.
