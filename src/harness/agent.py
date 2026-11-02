"""Component 2 & Harness: Google ADK Agent initialization and Model Provider resolution."""
from __future__ import annotations

import os
from typing import Optional

try:
    from google.adk.agents import Agent
except ImportError:
    class Agent:
        def __init__(self, name: str, model: str, description: str, instruction: str, tools: list):
            self.name = name
            self.model = model
            self.description = description
            self.instruction = instruction
            self.tools = tools

from .config import HarnessConfig
from .context import ContextBuilder


def get_agent_model(config: Optional[HarnessConfig] = None) -> str:
    """Resolves the configured model name based on provider setting."""
    cfg = config or HarnessConfig.from_env()
    if cfg.model_provider == "gemma":
        return cfg.gemma_model
    return cfg.gemini_model


_config = HarnessConfig.from_env()
_context_builder = ContextBuilder(policy_path=_config.policy_path)

root_agent = Agent(
    name="reverse_logistics_agent",
    model=os.getenv("ADK_MODEL", get_agent_model(_config)),
    description="Agente autonomo per la gestione resi, rimborsi d'eccezione e logistica inversa fashion.",
    instruction=_context_builder.build_system_instruction(),
    tools=[],
)
