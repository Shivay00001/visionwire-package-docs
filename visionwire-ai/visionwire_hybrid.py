import requests
import json
from visionwire_universal_config import OPENROUTER_API_KEY, OPENROUTER_URL

class VisionWireHybrid:
    def __init__(self):
        self.api_key = OPENROUTER_API_KEY

    def generate_content(self, context_prompt):
        if not self.api_key or self.api_key == "your_api_key_here":
            return self._mock_llm_response(context_prompt)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "google/gemini-2.0-flash-exp:free",
            "messages": [
                {"role": "system", "content": "You are VisionWire AI, an expert educational tutor. Generate structured study material."},
                {"role": "user", "content": context_prompt}
            ]
        }

        try:
            response = requests.post(OPENROUTER_URL, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"⚠️ API Error: {e}. Falling back to mock response.")
            return self._mock_llm_response(context_prompt)

    def _mock_llm_response(self, prompt):
        return f"### AI Generated Content\nBased on your request: {prompt[:100]}...\n\nThis is a placeholder for AI-generated educational content. Please configure a valid OpenRouter API key in .env to see real generations."
