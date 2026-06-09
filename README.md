# my-ai-agent

A small, production-minded command-line AI agent scaffold that works offline by default and can be connected to an OpenAI-compatible Chat Completions API for real-world use.

## What is included

- **Offline-safe default provider** for local development, CI, and demos without API keys.
- **OpenAI-compatible provider** configurable with environment variables.
- **CLI commands** for prompting the agent, running safe calculations, reading workspace files, and checking configuration health.
- **Safe local tools** with arithmetic-only expression evaluation and workspace path traversal protection.
- **JSONL memory** to persist recent user, tool, and assistant messages.
- **Automated tests** covering core agent behavior, CLI behavior, and security boundaries.

## Quick start

Run directly from a checkout without installation:

```bash
PYTHONPATH=src python -m my_ai_agent doctor
PYTHONPATH=src python -m my_ai_agent ask "calc: 2 * (3 + 4)"
```

Or install the console script in a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
my-ai-agent doctor
my-ai-agent ask "calc: 2 * (3 + 4)"
```

## Using a real model provider

By default the agent uses `MY_AI_AGENT_PROVIDER=mock`. To call an OpenAI-compatible endpoint:

```bash
export MY_AI_AGENT_PROVIDER=openai
export OPENAI_API_KEY="your-api-key"
export MY_AI_AGENT_MODEL="gpt-4.1-mini"
my-ai-agent ask "Draft a concise project status update"
```

Optional environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `MY_AI_AGENT_PROVIDER` | `mock` | `mock`, `openai`, or `openai-compatible`. |
| `MY_AI_AGENT_MODEL` | `gpt-4.1-mini` | Model name passed to the provider. |
| `MY_AI_AGENT_TEMPERATURE` | `0.2` | Sampling temperature. |
| `MY_AI_AGENT_TIMEOUT` | `30` | Provider request timeout in seconds. |
| `MY_AI_AGENT_MAX_RETRIES` | `2` | Retry attempts for transient provider failures. |
| `MY_AI_AGENT_MEMORY` | `.agent-memory.jsonl` | JSONL memory file path. |
| `MY_AI_AGENT_WORKSPACE` | current directory | Root directory for workspace file reads. |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | Base URL for OpenAI-compatible APIs. |
| `OPENAI_API_KEY` | unset | API key required for the OpenAI provider. |

## CLI reference

```bash
my-ai-agent doctor
my-ai-agent ask "Summarize this repo\nread: README.md"
my-ai-agent calc "(10 + 5) / 3"
my-ai-agent read README.md
```

Inline tool directives supported by `ask`:

- `calc: 2 + 2`
- `read: README.md`

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m compileall src tests
```

## Security notes

This project intentionally keeps tools conservative:

- Calculator expressions are parsed with `ast` and only arithmetic nodes are allowed.
- File reads are restricted to the configured workspace and return bounded text.
- The default provider is deterministic and does not send data over the network.
