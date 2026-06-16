
import unittest
from pathlib import Path
import os
import json
from my_ai_agent.tools import Calculator, WorkspaceReader
from my_ai_agent.memory import JsonlMemory, Message

class TestSecurityVulnerabilities(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
        self.workspace = Path("test_security_ws")
        self.workspace.mkdir(exist_ok=True)
        self.reader = WorkspaceReader(self.workspace)
        self.memory_path = Path("test_memory.jsonl")
        self.memory = JsonlMemory(self.memory_path)

    def tearDown(self):
        if self.workspace.exists():
            for file in self.workspace.iterdir():
                file.unlink()
            self.workspace.rmdir()
        if self.memory_path.exists():
            self.memory_path.unlink()

    def test_calculator_exponent_limit(self):
        # Exponent too large should fail gracefully
        result = self.calc.run("2**1001")
        self.assertFalse(result.ok)
        self.assertIn("Exponent too large", result.output)

    def test_calculator_magnitude_limit(self):
        # Result magnitude too large should fail gracefully
        result = self.calc.run("10**101")
        self.assertFalse(result.ok)
        self.assertIn("Result magnitude too large", result.output)

    def test_workspace_reader_memory_safe(self):
        # Create a large file
        large_file = self.workspace / "large.txt"
        with open(large_file, "wb") as f:
            f.seek(10 * 1024 * 1024 - 1) # 10MB
            f.write(b"Z")

        # This should be fast and memory-efficient
        result = self.reader.run("large.txt", max_chars=10)
        self.assertTrue(result.ok)
        self.assertEqual(len(result.output), 10)

    def test_jsonl_memory_oom_safe(self):
        # Create a large memory file
        with open(self.memory_path, "w", encoding="utf-8") as f:
            for i in range(10000):
                f.write(json.dumps({"role": "user", "content": f"message {i}"}) + "\n")

        # Should only load the last 5 messages efficiently
        messages = self.memory.load(limit=5)
        self.assertEqual(len(messages), 5)
        self.assertEqual(messages[0].content, "message 9995")
        self.assertEqual(messages[-1].content, "message 9999")

if __name__ == "__main__":
    unittest.main()
