"""VisionWire LLM client — REAL LLM calls only.

Reads the API key from the environment (OPENROUTER_API_KEY). There is no
mock/fallback response: if no key is configured, or the API call fails,
generate_content() raises an error saying so honestly.
"""
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
REQUEST_TIMEOUT = 60


class VisionWireHybrid:
    def __init__(self, api_key=None, model="google/gemini-2.0-flash-exp:free"):
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY", "")
        self.model = model

    def generate_content(self, context_prompt):
        if not self.api_key or self.api_key in ("your_api_key_here", "sk-placeholder"):
            raise RuntimeError(
                "No LLM API key configured. Set OPENROUTER_API_KEY in the "
                "environment (or .env) to generate real AI content."
            )
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system",
                 "content": "You are VisionWire AI, an expert educational tutor. Generate structured study material."},
                {"role": "user", "content": context_prompt},
            ],
        }
        response = requests.post(OPENROUTER_URL, headers=headers,
                                 data=json.dumps(payload), timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
