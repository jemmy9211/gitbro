from openai import OpenAI
import requests
import google.generativeai as genai
from abc import ABC, abstractmethod
from typing import Optional
from langchain_ollama import OllamaLLM
from config import config

class BaseProvider(ABC):
    """Base class for AI providers."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, temperature: float = 0.7):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self._system_prompt_override = None
    
    @abstractmethod
    def generate_message(self, diff: str) -> str:
        """Generate a commit message from a git diff."""
        pass
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for commit message generation."""
        if self._system_prompt_override:
            return self._system_prompt_override
        
        return (
            "Your task is to write a Git commit message based on the provided code diff. "
            "The message should follow standard conventions:\n"
            "- Start with a short imperative subject line (e.g., 'Fix bug', 'Add feature').\n"
            "- The subject line should be 50 characters or less if possible.\n"
            "- Optionally, provide a more detailed explanatory text after the subject line, separated by a blank line.\n"
            "- Your output should *only* be the commit message content, with no other surrounding text, titles, or explanations."
        )

class OpenAIProvider(BaseProvider):
    """OpenAI provider for GPT models."""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", temperature: float = 0.7):
        super().__init__(api_key, model, temperature)
        self.client = OpenAI(api_key=self.api_key)
    
    def generate_message(self, diff: str) -> str:
        """Generate commit message using OpenAI API."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": f"Code Diff: {diff}\n\nCommit Message:"}
                ],
                temperature=self.temperature,
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

class GeminiProvider(BaseProvider):
    """Google Gemini provider."""
    
    def __init__(self, api_key: str, model: str = "gemini-pro", temperature: float = 0.7):
        super().__init__(api_key, model, temperature)
        genai.configure(api_key=self.api_key)
        self.client = genai.GenerativeModel(self.model)
    
    def generate_message(self, diff: str) -> str:
        """Generate commit message using Gemini API."""
        try:
            prompt = f"{self._get_system_prompt()}\n\nCode Diff: {diff}\n\nCommit Message:"
            
            generation_config = genai.types.GenerationConfig(
                temperature=self.temperature,
                max_output_tokens=150,
            )
            
            response = self.client.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            if not response.text:
                raise Exception("No response generated")
            
            return response.text.strip()
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")

class ClaudeProvider(BaseProvider):
    """Anthropic Claude provider."""
    
    def __init__(self, api_key: str, model: str = "claude-3-haiku-20240307", temperature: float = 0.7):
        super().__init__(api_key, model, temperature)
        self.base_url = "https://api.anthropic.com/v1/messages"
    
    def generate_message(self, diff: str) -> str:
        """Generate commit message using Claude API."""
        try:
            headers = {
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01"
            }
            
            data = {
                "model": self.model,
                "max_tokens": 150,
                "temperature": self.temperature,
                "system": self._get_system_prompt(),
                "messages": [
                    {
                        "role": "user", 
                        "content": f"Code Diff: {diff}\n\nCommit Message:"
                    }
                ]
            }
            
            response = requests.post(self.base_url, headers=headers, json=data)
            
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
            
            result = response.json()
            if "content" not in result or not result["content"]:
                raise Exception("No response generated")
            
            return result["content"][0]["text"].strip()
        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")

class OllamaProvider(BaseProvider):
    """Ollama provider for local models."""
    
    def __init__(self, model: str = "llama3.2", temperature: float = 0.7, base_url: str = "http://localhost:11434"):
        super().__init__(None, model, temperature)
        self.base_url = base_url
    
    def generate_message(self, diff: str) -> str:
        """Generate commit message using Ollama."""
        try:
            llm = OllamaLLM(
                model=self.model,
                base_url=self.base_url,
                temperature=self.temperature
            )
            
            prompt = f"{self._get_system_prompt()}\n\nCode Diff: {diff}\n\nCommit Message:"
            response = llm.invoke(prompt)
            
            if hasattr(response, 'content'):
                return str(response.content).strip()
            return str(response).strip()
        except Exception as e:
            raise Exception(f"Ollama error: {str(e)}")

def get_provider(provider_name: str = None) -> BaseProvider:
    """Get a provider instance based on configuration."""
    if provider_name is None:
        provider_name = config.get_provider()
    
    if not provider_name:
        raise Exception("No provider configured. Please run with --setup first.")
    
    model = config.get_model(provider_name)
    temperature = config.get_temperature()
    
    if provider_name == "openai":
        api_key = config.get_api_key("openai")
        if not api_key:
            raise Exception("OpenAI API key not configured. Please run with --setup.")
        return OpenAIProvider(api_key, model, temperature)
    
    elif provider_name == "gemini":
        api_key = config.get_api_key("gemini")
        if not api_key:
            raise Exception("Gemini API key not configured. Please run with --setup.")
        return GeminiProvider(api_key, model, temperature)
    
    elif provider_name == "claude":
        api_key = config.get_api_key("claude")
        if not api_key:
            raise Exception("Claude API key not configured. Please run with --setup.")
        return ClaudeProvider(api_key, model, temperature)
    
    elif provider_name == "ollama":
        return OllamaProvider(model, temperature)
    
    else:
        raise Exception(f"Unknown provider: {provider_name}") 