"""Component 2 & Harness Orchestration: Google ADK Agent & Full Reverse Logistics Pipeline."""
from __future__ import annotations

import json
import os
import time
from typing import Any, Callable, Dict, Optional

# Attempt import from Google ADK; provide graceful shim if not yet installed in runtime
try:
    from google.adk.agents import Agent  # type: ignore
except ImportError:
    class Agent:  # type: ignore
        """Fallback Agent class when running in pre-install or offline unit tests."""
        def __init__(self, name: str, model: str, description: str, instruction: str, tools: list):
            self.name = name
            self.model = model
            self.description = description
            self.instruction = instruction
            self.tools = tools

from .config import HarnessConfig
from .context import ContextBuilder, CustomerTicket
from .policy_gate import PolicyGate, PolicyGateDecision, PolicyGateResult
from .tools import calculate_depreciated_refund, generate_wms_return_label
from .verifier import ReturnAuthorization, ReturnAuthorizationVerifier, VerificationError
from .constraints import ConstraintManager, ConstraintExceededError
from .observability import ExecutionTelemetry, HarnessTelemetry


def get_agent_model(config: Optional[HarnessConfig] = None) -> str:
    """Resolves the configured model name based on provider setting."""
    cfg = config or HarnessConfig.from_env()
    if cfg.model_provider == "gemma":
        return cfg.gemma_model
    return cfg.gemini_model


_config = HarnessConfig.from_env()
_context_builder = ContextBuilder(policy_path=_config.policy_path)

# Standard Google ADK Agent export for ADK Web UI / ADK CLI
root_agent = Agent(
    name="reverse_logistics_agent",
    model=os.getenv("ADK_MODEL", get_agent_model(_config)),
    description="Agente autonomo per la gestione resi, rimborsi d'eccezione e logistica inversa fashion.",
    instruction=_context_builder.build_system_instruction(),
    tools=[calculate_depreciated_refund, generate_wms_return_label],
)


class ReverseLogisticsHarness:
    """
    Complete 7-component Harness orchestrator:
    1. Context Builder
    2. LLM / Agent
    3. Policy Gate (HITL)
    4. Tools / Runtime
    5. Verifier
    6. Constraints
    7. Observability
    """

    def __init__(
        self,
        config: Optional[HarnessConfig] = None,
        llm_caller: Optional[Callable[[str, list[str]], str]] = None,
    ):
        self.config = config or HarnessConfig.from_env()
        self.context_builder = ContextBuilder(policy_path=self.config.policy_path)
        self.policy_gate = PolicyGate(
            refund_threshold=self.config.hitl_refund_threshold,
            fraud_risk_threshold=self.config.fraud_risk_threshold,
        )
        self.verifier = ReturnAuthorizationVerifier(warehouses_path=self.config.warehouses_path)
        self.constraints = ConstraintManager(max_steps=self.config.max_decision_steps)
        self.telemetry = HarnessTelemetry()
        self.llm_caller = llm_caller

    def execute_ticket(
        self,
        ticket: CustomerTicket,
        mock_cached_tokens: int = 1500,
    ) -> Dict[str, Any]:
        """
        Executes the ticket through the full 7-component harness pipeline.
        """
        start_time = time.time()
        self.constraints.reset()

        # Step 1: Constraint check
        self.constraints.record_step("context_assembly")

        # Step 2: Context Builder (Stable Zone + Volatile Zone)
        prompt = self.context_builder.build_prompt(ticket)

        # Step 3: LLM Execution or Deterministic Simulation
        self.constraints.record_step("llm_evaluation")

        raw_decision: Dict[str, Any]
        if self.llm_caller:
            raw_response = self.llm_caller(prompt, ticket.image_paths)
            try:
                raw_decision = json.loads(raw_response)
            except Exception:
                raw_decision = {"error": "Invalid LLM output", "raw": raw_response}
        else:
            # Deterministic default business logic for offline test execution
            raw_decision = self._simulate_agent_decision(ticket)

        # Step 4: Tools calculation (Depreciation)
        calc_result = calculate_depreciated_refund(
            original_price=ticket.purchase_price,
            condition="seam_tear_repairable" if "strapp" in ticket.complaint_text.lower() else "intact_defect_origin",
            has_original_tags=ticket.has_original_tags,
            days_since_delivery=ticket.days_since_delivery,
        )

        proposed_amount = calc_result.get("approved_refund", 0.0)

        # Step 5: Policy Gate (HITL check)
        gate_result = self.policy_gate.evaluate(
            ticket_id=ticket.ticket_id,
            refund_amount=proposed_amount,
            fraud_risk_score=ticket.fraud_risk_score,
            customer_id=ticket.customer_id,
        )

        if gate_result.is_blocked:
            action = "HITL_ESCALATION"
            warehouse = "WMS-MIL-01"
            reason = gate_result.reason
        else:
            action = "REFUND"
            warehouse = "WMS-LON-03" if ticket.country.upper() in {"UK", "GB"} else "WMS-MIL-01"
            reason = calc_result.get("reason", "Approved within policy.")

        # Step 6: Verifier
        raw_auth_payload = {
            "ticket_id": ticket.ticket_id,
            "action": action,
            "approved_amount": proposed_amount,
            "warehouse_code": warehouse,
            "reason": reason,
            "customs_declaration_required": (ticket.country.upper() in {"UK", "GB"}),
            "customs_notes": "Returned Goods Relief under UK-EU trade agreement" if ticket.country.upper() in {"UK", "GB"} else None,
        }

        verified_auth = self.verifier.verify(raw_auth_payload, origin_country=ticket.country)

        # Step 7: Observability
        prompt_tokens = len(prompt.split()) * 2  # Approximate token metric
        output_tokens = 120
        cached_tokens = min(mock_cached_tokens, prompt_tokens)

        tel = self.telemetry.record_execution(
            ticket_id=ticket.ticket_id,
            start_time=start_time,
            prompt_tokens=prompt_tokens,
            output_tokens=output_tokens,
            cached_content_tokens=cached_tokens,
            policy_gate_triggered=gate_result.is_blocked,
            status="HITL_ESCALATED" if gate_result.is_blocked else "COMPLETED",
        )

        return {
            "authorization": verified_auth,
            "gate_result": gate_result,
            "tool_calculation": calc_result,
            "telemetry": tel,
        }

    def _simulate_agent_decision(self, ticket: CustomerTicket) -> Dict[str, Any]:
        return {
            "ticket_id": ticket.ticket_id,
            "condition": "seam_tear_repairable",
            "recommended_action": "REFUND",
        }

