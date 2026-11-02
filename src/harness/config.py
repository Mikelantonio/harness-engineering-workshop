"""Configuration module for the Harness Engineering Workshop."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class HarnessConfig:
    """Central configuration for models, thresholds, and runtime policies."""
    model_provider: str = "gemini"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    ollama_base_url: str = "http://localhost:11434"
    gemma_model: str = "gemma2:9b"
    hitl_refund_threshold: float = 500.0
    fraud_risk_threshold: int = 70
    max_decision_steps: int = 3
    policy_path: Path = Path(__file__).resolve().parent.parent.parent / "assets" / "policies" / "return_policy_global.md"
    warehouses_path: Path = Path(__file__).resolve().parent.parent.parent / "assets" / "data" / "warehouses.json"

    @classmethod
    def from_env(cls) -> HarnessConfig:
        """Load configuration from environment variables with sensible defaults."""
        return cls(
            model_provider=os.getenv("MODEL_PROVIDER", "gemini").lower(),
            gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
            gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            gemma_model=os.getenv("GEMMA_MODEL", "gemma2:9b"),
            hitl_refund_threshold=float(os.getenv("HITL_REFUND_THRESHOLD", "500.0")),
            fraud_risk_threshold=int(os.getenv("FRAUD_RISK_THRESHOLD", "70")),
            max_decision_steps=int(os.getenv("MAX_DECISION_STEPS", "3")),
        )

