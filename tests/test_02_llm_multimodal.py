"""Tests for Component 2: LLM Agent & Multimodal Defect Inspection."""
from __future__ import annotations

import os
import unittest
from pathlib import Path
from src.harness.agent import root_agent, get_agent_model
from src.harness.config import HarnessConfig
from src.harness.context import ContextBuilder


class TestLLMMultimodal(unittest.TestCase):
    def test_agent_initialization_and_metadata(self):
        """Verifies that the Google ADK Agent is configured with required name and tools."""
        self.assertEqual(root_agent.name, "reverse_logistics_agent")
        # Ensure system instruction is wired directly from ContextBuilder
        expected_instruction = ContextBuilder().build_system_instruction()
        self.assertEqual(root_agent.instruction, expected_instruction)

    def test_model_resolution_gemini_vs_gemma(self):
        """Verifies dynamic resolution between Gemini and Gemma/Ollama."""
        cfg_gemini = HarnessConfig(model_provider="gemini", gemini_model="gemini-2.5-flash")
        self.assertEqual(get_agent_model(cfg_gemini), "gemini-2.5-flash")

        cfg_gemma = HarnessConfig(model_provider="gemma", gemma_model="gemma2:9b")
        self.assertEqual(get_agent_model(cfg_gemma), "gemma2:9b")

    def test_sample_defect_images_exist(self):
        """Verifies that multimodal sample image assets are in place on disk."""
        assets_dir = Path(__file__).resolve().parent.parent / "assets" / "images"
        jacket_img = assets_dir / "leather_jacket_tear.jpg"
        sneaker_img = assets_dir / "clean_sneakers.jpg"

        self.assertTrue(jacket_img.exists(), f"Missing test asset {jacket_img}")
        self.assertTrue(sneaker_img.exists(), f"Missing test asset {sneaker_img}")
        self.assertGreater(jacket_img.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()

