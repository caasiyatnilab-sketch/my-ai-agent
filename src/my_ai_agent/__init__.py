"""Production-minded command-line AI agent package."""

from .agent import Agent, AgentResult
from .config import AgentConfig

__all__ = ["Agent", "AgentConfig", "AgentResult"]
__version__ = "0.1.0"
