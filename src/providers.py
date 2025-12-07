"""AI Providers for commit message generation."""

from abc import ABC, abstractmethod
from typing import Optional
import requests

from openai import OpenAI
import google.generativeai as genai

from .config import config


class BaseProvider(ABC):
    """Base class for AI providers."""

    def __init__(self, model: str, temperature: float = 0.7):
        self.model = model
        self.temperature = temperature

    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = None) -> str:
        """Generate response from the AI provider."""
        pass

    def _default_system_prompt(self) -> str:
        return (
            "Write a Git commit message for this diff. "
            "Use imperative mood, keep subject ≤50 chars. "
            "Output only the commit message."
        )


class OpenAIProvider(BaseProvider):
    """OpenAI GPT provider."""

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", temperature: float = 0.7):
        super().__init__(model, temperature)
        self.client = OpenAI(api_key=api_key)

    def generate(self, prompt: str, system_prompt: str = None) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt or self._default_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()


class GeminiProvider(BaseProvider):
    """Google Gemini provider."""

    def __init__(self, api_key: str, model: str = "gemini-pro", temperature: float = 0.7):
        super().__init__(model, temperature)
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(model)

    def generate(self, prompt: str, system_prompt: str = None) -> str:
        full_prompt = f"{system_prompt or self._default_system_prompt()}\n\n{prompt}"
        response = self.client.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=self.temperature,
                max_output_tokens=200
            )
        )
        return response.text.strip()


class ClaudeProvider(BaseProvider):
    """Anthropic Claude provider."""

    API_URL = "https://api.anthropic.com/v1/messages"

    def __init__(self, api_key: str, model: str = "claude-3-haiku-20240307", temperature: float = 0.7):
        super().__init__(model, temperature)
        self.api_key = api_key

    def generate(self, prompt: str, system_prompt: str = None) -> str:
        response = requests.post(
            self.API_URL,
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": self.model,
                "max_tokens": 200,
                "temperature": self.temperature,
                "system": system_prompt or self._default_system_prompt(),
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        response.raise_for_status()
        return response.json()["content"][0]["text"].strip()


class OllamaProvider(BaseProvider):
    """Ollama local model provider (no langchain dependency)."""

    def __init__(self, model: str = "llama3.2", temperature: float = 0.7, base_url: str = "http://localhost:11434"):
        super().__init__(model, temperature)
        self.base_url = base_url

    def generate(self, prompt: str, system_prompt: str = None) -> str:
        full_prompt = f"{system_prompt or self._default_system_prompt()}\n\n{prompt}"
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "options": {"temperature": self.temperature}
            }
        )
        response.raise_for_status()
        return response.json()["response"].strip()


def get_provider(provider_name: str = None) -> BaseProvider:
    """Factory function to get configured provider instance."""
    name = provider_name or config.get_provider()
    if not name:
        raise RuntimeError("No provider configured. Run 'gitbro setup' first.")

    model = config.get_model(name)
    temp = config.get_temperature()

    providers = {
        "openai": lambda: OpenAIProvider(config.get_api_key("openai"), model, temp),
        "gemini": lambda: GeminiProvider(config.get_api_key("gemini"), model, temp),
        "claude": lambda: ClaudeProvider(config.get_api_key("claude"), model, temp),
        "ollama": lambda: OllamaProvider(model, temp),
    }

    if name not in providers:
        raise ValueError(f"Unknown provider: {name}")

    if name != "ollama" and not config.get_api_key(name):
        raise RuntimeError(f"{name.upper()} API key not configured. Run 'gitbro setup {name}'.")

    return providers[name]()
