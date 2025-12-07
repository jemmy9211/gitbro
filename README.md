# 🧠 gitbro

AI-powered Git CLI tool. Generate commit messages, branch names, changelogs, and more.

[![GitHub stars](https://img.shields.io/github/stars/jemmy9211/gitbro)](https://github.com/jemmy9211/gitbro)

## Installation

```bash
# Clone and install
git clone https://github.com/jemmy9211/gitbro.git
cd gitbro
pip install -e .

# Or use the install script
./install.sh
```

## Setup

```bash
gitbro setup          # Interactive provider selection
gitbro setup ollama   # Direct setup (openai/gemini/claude/ollama)
```

**Supported Providers:**
| Provider | API Key | Cost |
|----------|---------|------|
| OpenAI | [Get key](https://platform.openai.com/api-keys) | Pay per use |
| Gemini | [Get key](https://makersuite.google.com/app/apikey) | Free tier |
| Claude | [Get key](https://console.anthropic.com/account/keys) | Pay per use |
| Ollama | Not needed | Free (local) |

## Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `gitbro commit` | `c` | Generate AI commit message |
| `gitbro branch` | `b` | Suggest branch name |
| `gitbro explain` | `e` | Explain code changes |
| `gitbro summarize` | `s` | Summarize commit history |
| `gitbro validate` | `v` | Validate commit messages |
| `gitbro add` | `a` | AI-assisted staging |
| `gitbro graph` | `g` | Open Git graph in browser |
| `gitbro clean` | - | Clean merged branches |
| `gitbro hook` | - | Install pre-commit hook |
| `gitbro status` | - | Show config |

## Quick Examples

```bash
# Generate commit message
git add .
gitbro c                    # Basic
gitbro c -c                 # Conventional Commits format
gitbro c -a                 # Auto-commit

# Branch naming
gitbro b                    # Suggest name
gitbro b -c                 # Create suggested branch

# Explain changes
gitbro e                    # Working directory
gitbro e -s                 # Staged only
gitbro e -f src/main.py     # Specific file

# Summarize history
gitbro s                              # Summary
gitbro s --format changelog           # Changelog
gitbro s --format release --since v1.0.0  # Release notes

# Validate commits
gitbro v                    # Check last 10
gitbro v -c                 # Conventional format
gitbro v -c --fix           # Suggest fixes

# Clean branches
gitbro clean                # Local only
gitbro clean -r             # Include remote
gitbro clean -d             # Dry run

# Git graph (opens in browser)
gitbro g                    # Open graph viewer
gitbro g -n 200             # Show 200 commits
gitbro g -p 9000            # Use port 9000
```

## Configuration
## Configuration

Config stored at `~/.gitbro/config.json`:

```json
{
  "provider": "ollama",
  "settings": {
    "temperature": 0.7,
    "model": { "ollama": "llama3.2" }
  }
}
```

**Temperature:** 0.0 (conservative) → 2.0 (creative)

## Shell Aliases

```bash
# Add to ~/.bashrc or ~/.zshrc
alias gc='gitbro c -c'
alias gb='gitbro b'
alias ge='gitbro e'
```

## Troubleshooting

```bash
# Check status
gitbro status

# Ollama not responding?
ollama serve              # Start Ollama server

# No staged changes?
git add .                 # Stage first
```

## License

MIT
