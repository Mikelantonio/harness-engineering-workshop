"""Test fixtures and mock helpers for the Harness Engineering Workshop."""
import os
import sys
from pathlib import Path

# Ensure root directory is on sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from src.harness.context import CustomerTicket
except ImportError:
    # CustomerTicket is implemented in Step 1 (Context Builder).
    # Graceful fallback allows step-0 tests to run without harness imports.
    CustomerTicket = None

try:
    import pytest
    fixture = pytest.fixture
except ImportError:
    # Minimal fixture decorator fallback for standalone unittest runs
    def fixture(func):
        return func


@fixture
def sample_standard_ticket():
    """A standard compliant return request under €500."""
    if CustomerTicket is None:
        return None
    return CustomerTicket(
        ticket_id="TICK-IT-101",
        customer_id="CUST-4421",
        country="IT",
        item_category="leather",
        item_description="Giacca in pelle marrone taglia M",
        purchase_price=180.0,
        days_since_delivery=12,
        complaint_text="Cucitura della tasca destra leggermente scucita.",
        has_original_tags=True,
        fraud_risk_score=15,
        image_paths=[str(ROOT_DIR / "assets" / "images" / "leather_jacket_tear.jpg")],
    )


@fixture
def sample_high_value_ticket():
    """A luxury return exceeding €500 threshold requiring HITL."""
    if CustomerTicket is None:
        return None
    return CustomerTicket(
        ticket_id="TICK-FR-202",
        customer_id="CUST-8899",
        country="FR",
        item_category="luxury",
        item_description="Cappotto in Cashmere Loro Piana",
        purchase_price=850.0,
        days_since_delivery=10,
        complaint_text="Difetto visibile sulla fodera interna.",
        has_original_tags=True,
        fraud_risk_score=20,
        image_paths=[str(ROOT_DIR / "assets" / "images" / "leather_jacket_tear.jpg")],
    )


@fixture
def sample_fraud_risk_ticket():
    """A ticket from a high-fraud-risk account requiring immediate fraud halt."""
    if CustomerTicket is None:
        return None
    return CustomerTicket(
        ticket_id="TICK-DE-303",
        customer_id="CUST-SUSPECT-77",
        country="DE",
        item_category="denim",
        item_description="Jeans modello Slim Fit",
        purchase_price=120.0,
        days_since_delivery=5,
        complaint_text="Dichiara pacco arrivato senza articolo.",
        has_original_tags=False,
        fraud_risk_score=85,
    )


@fixture
def sample_uk_cross_border_ticket():
    """A return originating from the UK requiring customs declaration and London hub."""
    if CustomerTicket is None:
        return None
    return CustomerTicket(
        ticket_id="TICK-UK-404",
        customer_id="CUST-UK-1290",
        country="UK",
        item_category="knitwear",
        item_description="Maglione lana merino",
        purchase_price=220.0,
        days_since_delivery=14,
        complaint_text="Taglia errata rispetto alla guida sul sito.",
        has_original_tags=True,
        fraud_risk_score=10,
    )

