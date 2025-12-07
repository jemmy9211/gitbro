"""
Message generation utilities.
This module is kept for backward compatibility but the main CLI is in cli.py.
"""

from .config import config
from .providers import get_provider


def generate_message(diff: str, conventional: bool = False) -> str:
    """Generate a commit message from a git diff."""
    provider = get_provider()

    if conventional:
        prompt = (
            "Write a Conventional Commits message: type(scope): description. "
            "Types: feat, fix, docs, style, refactor, test, chore. Output only the message."
        )
    else:
        prompt = "Write a concise Git commit message. Use imperative mood, ≤50 chars. Output only the message."

    return provider.generate(diff, prompt)


# Backward compatibility - redirect to new CLI
def main():
    """Entry point - redirects to new CLI."""
    from .cli import main as cli_main
    cli_main()


if __name__ == "__main__":
    main()
