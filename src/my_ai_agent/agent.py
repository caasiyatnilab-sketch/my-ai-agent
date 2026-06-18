"""Agent orchestration."""

from __future__ import annotations

from dataclasses import dataclass

from .config import AgentConfig
from .memory import JsonlMemory
from .providers import Message, Provider, build_provider
from .tools import Calculator, ToolResult, WorkspaceReader


@dataclass(frozen=True)
class AgentResult:
    """Result returned by an agent run."""

    answer: str
    tool_results: list[ToolResult]


class Agent:
    """Small but practical agent with provider abstraction, memory, and safe tools."""

    def __init__(self, config: AgentConfig | None = None, provider: Provider | None = None) -> None:
        self.config = config or AgentConfig.from_env()
        self.provider = provider or build_provider(self.config)
        self.memory = JsonlMemory(self.config.memory_path)
        self.calculator = Calculator()
        self.reader = WorkspaceReader(self.config.workspace)

    def ask(self, prompt: str, *, use_memory: bool = True) -> AgentResult:
        """Ask the configured model a question and persist the exchange."""

        tool_results = self._run_inline_tools(prompt)
        tool_context = "\n".join(
            f"Tool: {result.name}\nOK: {result.ok}\nOutput: {result.output}"
            for result in tool_results
        )
        user_content = prompt if not tool_context else f"{prompt}\n\nTool results:\n{tool_context}"
        messages = [Message("system", self.config.system_prompt)]
        if use_memory:
            messages.extend(self.memory.load())
        messages.append(Message("user", user_content))
        answer = self.provider.complete(messages)

        # Store the exact user content sent to the provider to maintain consistency
        # and avoid using role: 'tool' which is not supported by our simple provider.
        self.memory.append(Message("user", user_content))
        self.memory.append(Message("assistant", answer))
        return AgentResult(answer=answer, tool_results=tool_results)

    def calculate(self, expression: str) -> ToolResult:
        """Run the calculator tool directly."""

        return self.calculator.run(expression)

    def read_file(self, relative_path: str) -> ToolResult:
        """Run the workspace reader tool directly."""

        return self.reader.run(relative_path)

    def _run_inline_tools(self, prompt: str) -> list[ToolResult]:
        """Support simple inline tool directives for real-world CLI automation.

        Directives:
        - ``calc: 2 + 2``
        - ``read: README.md``
        """

        results: list[ToolResult] = []
        for raw_line in prompt.splitlines():
            line = raw_line.strip()
            lowered = line.lower()
            if lowered.startswith("calc:"):
                results.append(self.calculate(line.split(":", 1)[1].strip()))
            elif lowered.startswith("read:"):
                results.append(self.read_file(line.split(":", 1)[1].strip()))
        return results
