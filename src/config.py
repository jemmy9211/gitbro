import os
import json
from pathlib import Path
from typing import Dict, Optional
import getpass

class Config:
    """Configuration manager for API providers and settings."""
    
    def __init__(self):
        self.config_dir = Path.home() / '.gitbrain'
        self.config_file = self.config_dir / 'config.json'
        self.config_dir.mkdir(exist_ok=True)
        self._config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {
            'provider': None,
            'api_keys': {},
            'settings': {
                'temperature': 0.7,
                'max_tokens': 150,
                'model': {}
            }
        }
    
    def _save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self._config, f, indent=2)
            # Set secure file permissions (user read/write only)
            os.chmod(self.config_file, 0o600)
        except IOError as e:
            print(f"Warning: Could not save configuration: {e}")
    
    def get_provider(self) -> Optional[str]:
        """Get the currently selected provider."""
        return self._config.get('provider')
    
    def set_provider(self, provider: str):
        """Set the current provider."""
        valid_providers = ['openai', 'gemini', 'claude', 'ollama']
        if provider not in valid_providers:
            raise ValueError(f"Invalid provider. Must be one of: {valid_providers}")
        self._config['provider'] = provider
        self._save_config()
    
    def get_api_key(self, provider: str) -> Optional[str]:
        """Get API key for a provider."""
        return self._config['api_keys'].get(provider)
    
    def set_api_key(self, provider: str, api_key: str):
        """Set API key for a provider."""
        self._config['api_keys'][provider] = api_key
        self._save_config()
    
    def get_model(self, provider: str) -> str:
        """Get the model for a provider."""
        default_models = {
            'openai': 'gpt-3.5-turbo',
            'gemini': 'gemini-pro',
            'claude': 'claude-3-haiku-20240307',
            'ollama': 'llama3.2'
        }
        return self._config['settings']['model'].get(provider, default_models.get(provider, ''))
    
    def set_model(self, provider: str, model: str):
        """Set the model for a provider."""
        self._config['settings']['model'][provider] = model
        self._save_config()
    
    def get_temperature(self) -> float:
        """Get the temperature setting."""
        return self._config['settings']['temperature']
    
    def set_temperature(self, temperature: float):
        """Set the temperature setting."""
        self._config['settings']['temperature'] = max(0.0, min(2.0, temperature))
        self._save_config()
    
    def setup_provider(self, provider: str) -> bool:
        """Interactive setup for a provider."""
        print(f"\nSetting up {provider.upper()} provider...")
        
        if provider == 'ollama':
            # For Ollama, just check if it's running
            print("Ollama uses local models and doesn't require an API key.")
            model = input(f"Enter model name (default: {self.get_model(provider)}): ").strip()
            if model:
                self.set_model(provider, model)
            self.set_provider(provider)
            return True
        
        # For cloud providers, get API key
        current_key = self.get_api_key(provider)
        if current_key:
            print(f"API key already configured for {provider}")
            use_existing = input("Use existing API key? (y/n): ").strip().lower()
            if use_existing == 'y':
                self.set_provider(provider)
                return True
        
        print(f"\nPlease get your API key from:")
        urls = {
            'openai': 'https://platform.openai.com/api-keys',
            'gemini': 'https://makersuite.google.com/app/apikey',
            'claude': 'https://console.anthropic.com/account/keys'
        }
        print(f"  {urls.get(provider, 'the provider website')}")
        
        api_key = getpass.getpass(f"Enter your {provider.upper()} API key: ").strip()
        if not api_key:
            print("API key is required.")
            return False
        
        self.set_api_key(provider, api_key)
        
        # Set model if needed
        model = input(f"Enter model name (default: {self.get_model(provider)}): ").strip()
        if model:
            self.set_model(provider, model)
        
        self.set_provider(provider)
        print(f"✓ {provider.upper()} provider configured successfully!")
        return True
    
    def is_configured(self, provider: str = None) -> bool:
        """Check if a provider is configured."""
        if provider is None:
            provider = self.get_provider()
        if not provider:
            return False
        
        if provider == 'ollama':
            return True  # Ollama doesn't need API key
        
        return bool(self.get_api_key(provider))
    
    def list_providers(self) -> Dict[str, bool]:
        """List all providers and their configuration status."""
        providers = ['openai', 'gemini', 'claude', 'ollama']
        return {provider: self.is_configured(provider) for provider in providers}

# Global config instance
config = Config() 