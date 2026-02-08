# 🧠 gitbro

AI-powered Git CLI tool with a full interactive TUI. Manage your entire Git workflow — staging, committing, pushing, branching, stashing, and more — all enhanced with AI.

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

**Dependencies:** click, gitpython, openai, google-generativeai, requests, rich

## 🚀 Quick Start — Interactive TUI (Recommended)

Just run `gitbro` without any arguments:

```bash
gitbro
```

This launches an interactive **Rich-powered TUI** with a grid menu organized by workflow phase:

```
┌─────────────────────────────────────────┐
│ gitbro  AI-Powered Git Tool             │
└─────────────────────────────────────────┘

  -- workflow --
   1 status        2 diff          3 add           4 commit        5 push

  -- more git --
   6 pull          7 unstage       8 amend         9 stash        10 discard
  11 remove       12 branches     13 log

  -- ai --
  14 quick commit  15 ai explain  16 ai summarize 17 ai stage    18 validate

  -- tools --
  19 graph         20 clean       21 settings

   0 exit
```

No commands to remember — just pick a number!

### TUI Features at a Glance

| Section | Features |
|---------|----------|
| **Workflow** | Status overview · View diff (working/staged/last commit) · Stage files (all/pick/pattern) · AI commit message (standard or conventional) · Push (with auto-upstream and force-with-lease) |
| **More Git** | Pull (merge/rebase/fetch) · Unstage · Amend last commit · Stash (push/pop/apply/drop/with message) · Discard changes · Remove/untrack files · Branch ops (switch/create/AI-suggest/delete) · Commit log |
| **AI** | Quick Commit (stage all → AI message → commit) · AI explain changes · AI summarize history (summary/changelog/release notes) · AI-assisted staging (per-file analysis) · Validate commit messages with AI fix suggestions |
| **Tools** | Git graph in browser · Clean merged branches (local + remote) · Settings (provider/model/temperature) |

## Setup

First run will guide you through provider setup automatically. You can also configure manually:

```bash
gitbro setup        # Interactive setup
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
| `gitbro` | | **Interactive TUI** (recommended) |
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
