"""Wrapper around Hugging Face image generation endpoints."""

from __future__ import annotations

import os

import requests


class HuggingFaceClient:
    def __init__(self, token: str | None = None, model: str | None = None) -> None:
        self.token = token or os.getenv("HUGGINGFACE_TOKEN", "")
        self.model = model or os.getenv("HF_IMAGE_MODEL", "Qwen/Qwen-Image")
        self.base_url = os.getenv("HF_API_BASE", "https://api-inference.huggingface.co/models")

    def generate_image(self, *, prompt: str) -> bytes:
        if not self.token:
            raise RuntimeError("Hugging Face token missing")
        url = f"{self.base_url}/{self.model}"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(url, headers=headers, json={"inputs": prompt})
        response.raise_for_status()
        return response.content
