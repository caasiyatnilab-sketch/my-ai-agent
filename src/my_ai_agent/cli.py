"""Command-line interface for my-ai-agent."""

from __future__ import annotations

import argparse
import sys

from .agent import Agent
from .config import AgentConfig


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a practical local AI agent.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ask = subparsers.add_parser("ask", help="Ask the agent a single prompt.")
    ask.add_argument(
        "prompt", nargs="+", help="Prompt text. Supports inline 'calc:' and 'read:' directives."
    )
    ask.add_argument(
        "--no-memory", action="store_true", help="Do not include previous memory in the request."
    )

    calc = subparsers.add_parser("calc", help="Evaluate a safe arithmetic expression.")
    calc.add_argument("expression", help="Expression to evaluate, e.g. '2 * (3 + 4)'.")

    read = subparsers.add_parser("read", help="Read a file inside the configured workspace.")
    read.add_argument("path", help="Workspace-relative file path to read.")

    subparsers.add_parser("doctor", help="Validate configuration and provider readiness.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    config = AgentConfig.from_env()

    try:
        agent = Agent(config)
        if args.command == "ask":
            if sys.stdout.isatty():
                sys.stdout.write("Thinking...")
                sys.stdout.flush()

            try:
                result = agent.ask(" ".join(args.prompt), use_memory=not args.no_memory)
            finally:
                if sys.stdout.isatty():
                    # Clear "Thinking..." indicator
                    sys.stdout.write("\r" + " " * 12 + "\r")
                    sys.stdout.flush()

            for tool_result in result.tool_results:
                status = "ok" if tool_result.ok else "error"
                print(f"[{tool_result.name}:{status}] {tool_result.output}")

            if result.tool_results:
                print()  # Spacer between tool results and final answer

            print(result.answer)
            return 0
        if args.command == "calc":
            result = agent.calculate(args.expression)
            print(result.output)
            return 0 if result.ok else 2
        if args.command == "read":
            result = agent.read_file(args.path)
            print(result.output)
            return 0 if result.ok else 2
        if args.command == "doctor":
            print(f"provider={config.provider}")
            print(f"model={config.model}")
            print(f"workspace={config.workspace}")
            print("status=ready")
            return 0
    except Exception as exc:  # noqa: BLE001 - CLI should report clean failures.
        print(f"error: {exc}", file=sys.stderr)
        return 1

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
