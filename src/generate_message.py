import subprocess
import sys
import argparse
from typing import Optional
from config import config
from providers import get_provider

class MessageGenerator:
    """Main message generator that uses configured providers."""
    
    def __init__(self):
        self.base_temperature = config.get_temperature()
        self.temperature_increment = 0.1
        self.max_temperature = 2.0
        self.current_temperature = self.base_temperature
        
    def increase_temperature(self):
        """Increase the temperature for more creative outputs."""
        self.current_temperature = min(
            self.current_temperature + self.temperature_increment,
            self.max_temperature
        )
        config.set_temperature(self.current_temperature)
        
    def reset_temperature(self):
        """Reset temperature to base value."""
        self.current_temperature = self.base_temperature
        config.set_temperature(self.current_temperature)

    def generate_message(self, diff: str) -> str:
        """Generate a commit message using the configured provider."""
        provider = get_provider()
        provider.temperature = self.current_temperature
        return provider.generate_message(diff)

# Global generator instance
generator = MessageGenerator()

def get_diff() -> Optional[str]:
    """Get the Git diff of staged changes."""
    result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing 'git diff --cached': {result.stderr.strip()}", file=sys.stderr)
        return None
    if result.stdout.strip() == "":
        print("No staged changes found. Please use 'git add' to stage your changes first.")
        return None
    return result.stdout

def generate_message(diff: str) -> str:
    """Generate a commit message using the configured provider."""
    return generator.generate_message(diff)

def increase_creativity():
    """Increase the temperature for next generation."""
    generator.increase_temperature()

def reset_creativity():
    """Reset the temperature to base value."""
    generator.reset_temperature()

def setup_provider(provider_name: str = None) -> bool:
    """Setup a provider interactively."""
    if provider_name:
        return config.setup_provider(provider_name)
    
    # Show available providers
    providers = config.list_providers()
    print("\nAvailable providers:")
    for i, (provider, is_configured) in enumerate(providers.items(), 1):
        status = "✓ Configured" if is_configured else "✗ Not configured"
        print(f"  {i}. {provider.upper()} - {status}")
    
    try:
        choice = input("\nSelect a provider (1-4): ").strip()
        provider_list = list(providers.keys())
        provider_index = int(choice) - 1
        
        if 0 <= provider_index < len(provider_list):
            selected_provider = provider_list[provider_index]
            return config.setup_provider(selected_provider)
        else:
            print("Invalid choice.")
            return False
    except (ValueError, KeyboardInterrupt):
        print("\nSetup cancelled.")
        return False

def show_status():
    """Show current configuration status."""
    current_provider = config.get_provider()
    print(f"\nCurrent provider: {current_provider.upper() if current_provider else 'None'}")
    
    providers = config.list_providers()
    print("\nProvider status:")
    for provider, is_configured in providers.items():
        status = "✓ Configured" if is_configured else "✗ Not configured"
        current = " (current)" if provider == current_provider else ""
        model = config.get_model(provider)
        print(f"  {provider.upper()}: {status}{current}")
        if is_configured and model:
            print(f"    Model: {model}")
    
    print(f"\nTemperature: {config.get_temperature()}")

def main():
    """Main function with CLI argument parsing."""
    parser = argparse.ArgumentParser(description="AI-powered Git commit message generator")
    parser.add_argument("--setup", nargs="?", const=True, 
                       help="Setup a provider (optionally specify: openai, gemini, claude, ollama)")
    parser.add_argument("--status", action="store_true", 
                       help="Show current configuration status")
    parser.add_argument("--provider", 
                       help="Set the active provider (openai, gemini, claude, ollama)")
    
    args = parser.parse_args()
    
    # Handle CLI arguments
    if args.status:
        show_status()
        return 0
    
    if args.setup is not None:
        provider_name = args.setup if isinstance(args.setup, str) else None
        if setup_provider(provider_name):
            print("\nSetup completed successfully!")
            return 0
        else:
            print("\nSetup failed.")
            return 1
    
    if args.provider:
        try:
            config.set_provider(args.provider)
            print(f"Active provider set to: {args.provider.upper()}")
            return 0
        except ValueError as e:
            print(f"Error: {e}")
            return 1
    
    # Check if a provider is configured
    if not config.get_provider() or not config.is_configured():
        print("No provider is configured. Please run with --setup first.")
        print("Example: python generate_message.py --setup openai")
        return 1
    
    # Generate commit message
    diff = get_diff()
    if diff is None:
        return 1
    
    try:
        message = generate_message(diff)
        print(message)
        return 0
    except Exception as e:
        print(f"Error generating commit message: {str(e)}")
        print("Try running with --setup to reconfigure your provider.")
        return 1

if __name__ == "__main__":
    exit(main())