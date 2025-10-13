"""Wrapper around OpenAI API for prompt generation."""

from __future__ import annotations

import os

import requests


class OpenAIClient:
    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    def generate_prompt(self, *, diary_text: str) -> dict:
        """Return a placeholder structured prompt to feed the image model."""

        if not self.api_key:
            raise RuntimeError("OpenAI API key missing")

        # TODO: replace with actual API call. Here we return a scaffold structure.
        return {
            "model": "gpt-4o-mini",
            "panels": [
                {"index": idx, "description": f"Panel {idx} inspired by diary."}
                for idx in range(1, 5)
            ],
        }
