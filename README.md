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

## 🚀 Quick Start — Interactive Mode (Recommended)

Just run `gitbro` without any arguments:

```bash
gitbro
```

This opens a **interactive menu** where you can:

```
┌──────────────────────────────────────────┐
│ 🧠 gitbro — AI-Powered Git Tool         │
└──────────────────────────────────────────┘

  What would you like to do?

  1. ⚡ Quick Commit       — stage all + AI message + commit
  2. 📝 Commit Message     — AI commit message for staged changes
  3. 🌿 Branch Name        — AI branch name from changes
  4. 📖 Explain Changes    — plain English explanation of diffs
  5. 📊 Summarize History  — changelog / release notes
  6. ✅ Validate Commits   — check commit message formats
  7. 📁 AI-Assisted Stage  — review & stage files with AI
  8. 🔀 Git Graph          — visual graph in browser
  9. 🧹 Clean Branches     — delete merged branches
  10. ⚙️  Settings          — provider, model, temperature
```

No need to remember any commands! Just pick a number.

## Setup

```bash
gitbro              # Interactive mode will guide you through setup
gitbro setup        # Or run setup directly
gitbro setup ollama # Direct setup (openai/gemini/claude/ollama)
```

**Supported Providers:**
| Provider | API Key | Cost |
|----------|---------|------|
| OpenAI | [Get key](https://platform.openai.com/api-keys) | Pay per use |
| Gemini | [Get key](https://makersuite.google.com/app/apikey) | Free tier |
| Claude | [Get key](https://console.anthropic.com/account/keys) | Pay per use |
| Ollama | Not needed | Free (local) |

## CLI Commands (Advanced)

All features are also available as direct commands for scripting/automation:

| Command | Alias | Description |
|---------|-------|-------------|
| `gitbro` | | **Interactive menu** (recommended) |
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

## CLI Examples

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
