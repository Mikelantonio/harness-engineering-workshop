from pathlib import Path
from runpy import run_path

# Load pure tool code without importing google-adk: tests are fully offline.
estimate_lab_time = run_path(str(Path(__file__).resolve().parents[1] / "hello_adk" / "tools.py"))["estimate_lab_time"]


def test_estimate_small_lab():
    result = estimate_lab_time(participants=12, steps=5)
    assert result["status"] == "success"
    assert result["total_minutes"] == 20


def test_estimate_big_lab_has_coordination_buffer():
    result = estimate_lab_time(participants=40, steps=5)
    assert result["total_minutes"] == 30


def test_invalid_inputs_are_rejected():
    assert estimate_lab_time(participants=0, steps=3)["status"] == "error"
    assert estimate_lab_time(participants=10, steps=True)["status"] == "error"
