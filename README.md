# 🧠 AI-Powered Git CLI Tool (gitbrain v2.0)

A comprehensive AI-assisted Git CLI tool that enhances developer workflow through smart commit handling, diff summarization, branch naming, validation, and more. Choose from OpenAI GPT models, Google Gemini, Anthropic Claude, or local Ollama models.

## 🚀 New in v2.0

- **Multiple Subcommands**: 8 powerful AI-assisted Git workflow commands
- **Semantic Branch Naming**: AI-generated branch names based on changes
- **Diff Explanations**: Plain English explanations of code changes
- **Commit History Summarization**: Generate changelogs and release notes
- **Commit Message Validation**: Check against Conventional Commits format
- **Interactive Staging**: AI-assisted `git add -p` experience
- **Pre-commit Hooks**: Automated validation and message generation
- **Enhanced CLI**: Built with Click for better user experience

## 🧰 Features & Commands

### Core Features

- **Multiple AI Providers**: OpenAI, Google Gemini, Anthropic Claude, and Ollama
- **Secure API Key Management**: Encrypted local storage of API credentials
- **Interactive Setup**: Easy configuration wizard for each provider
- **Creativity Control**: Adjust temperature for more or less creative outputs
- **Local & Cloud**: Use local models (Ollama) or cloud-based AI services
- **Cross-Platform**: Works on Linux, macOS, and Windows

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `commit` | Generate AI-powered commit messages | `gitbrain commit --conventional` |
| `branch-suggest` | Suggest semantic branch names | `gitbrain branch-suggest --create` |
| `explain` | Human-friendly diff explanations | `gitbrain explain --staged` |
| `summarize` | Commit history summarization | `gitbrain summarize --format changelog` |
| `validate` | Commit message format checking | `gitbrain validate --conventional --fix` |
| `interactive-add` | AI-assisted staging | `gitbrain interactive-add` |
| `clean-branches` | Clean merged local/remote branches | `gitbrain clean-branches --remote` |
| `install-hook` | Pre-commit hook integration | `gitbrain install-hook` |
| `setup` | Configure AI providers | `gitbrain setup ollama` |
| `status` | Show configuration status | `gitbrain status` |

## 📦 Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/gitbrain.git
   cd gitbrain
   ```

2. **Run the Installation Script:**
   ```bash
   ./install.sh
   ```
   This script:
   - Creates a Python virtual environment
   - Installs required dependencies (OpenAI, Anthropic, Google AI, Click, GitPython)
   - Sets up the executable script

3. **Set Up an AI Provider:**
   ```bash
   gitbrain setup
   ```
   Choose from the interactive menu or specify directly:
   ```bash
   gitbrain setup openai    # For OpenAI
   gitbrain setup gemini    # For Google Gemini
   gitbrain setup claude    # For Anthropic Claude
   gitbrain setup ollama    # For Ollama (local)
   ```

## 🎯 Quick Start Guide

### Getting Started with New Features

1. **Check your setup:**
   ```bash
   gitbrain status
   ```

2. **Make some changes and stage them:**
   ```bash
   echo "console.log('Hello AI!');" > hello.js
   git add hello.js
   ```

3. **Generate an AI commit message:**
   ```bash
   gitbrain commit
   # Output: Add hello.js with greeting message
   ```

4. **Get AI explanation of your changes:**
   ```bash
   gitbrain explain --staged
   # Output: 📝 Change Explanation:
   # This change adds a new JavaScript file that prints a greeting message to the console...
   ```

5. **Get a semantic branch name suggestion:**
   ```bash
   gitbrain branch-suggest
   # Output: Suggested branch name: feat/add-hello-script
   ```

## 🛠️ Command Reference

### `commit` - AI-Powered Commit Messages

Generate meaningful commit messages from staged changes.

```bash
# Basic usage
gitbrain commit

# Use Conventional Commits format
gitbrain commit --conventional

# Auto-commit without confirmation
gitbrain commit --auto

# Adjust creativity level
gitbrain commit --temperature 1.2
```

**Options:**
- `--temperature, -t`: AI creativity level (0.0-2.0)
- `--auto, -a`: Auto-commit with generated message
- `--conventional, -c`: Use Conventional Commits format

### `branch-suggest` - Semantic Branch Naming

Generate branch names based on code changes.

```bash
# Suggest branch name from staged changes
gitbrain branch-suggest

# Auto-create the suggested branch
gitbrain branch-suggest --create

# Generate name from specific commit
gitbrain branch-suggest --from-commit abc123
```

**Options:**
- `--create, -c`: Auto-create the suggested branch
- `--from-commit`: Generate name from specific commit hash

### `explain` - Code Change Explanations

Get plain English explanations of your code changes.

```bash
# Explain working directory changes
gitbrain explain

# Explain only staged changes
gitbrain explain --staged

# Explain changes in specific file
gitbrain explain --file src/main.py
```

**Options:**
- `--staged, -s`: Explain staged changes only
- `--file, -f`: Explain changes in specific file

### `summarize` - Commit History Analysis

Generate summaries, changelogs, and release notes from commit history.

```bash
# Basic summary of recent commits
gitbrain summarize

# Generate a changelog
gitbrain summarize --format changelog

# Create release notes
gitbrain summarize --format release-notes

# Filter by time period
gitbrain summarize --since "1 week ago"

# Filter by author
gitbrain summarize --author "john@example.com"

# Summarize specific branch
gitbrain summarize --branch feature/new-auth
```

**Options:**
- `--since`: Commits since date/commit (e.g., "1 week ago", commit hash)
- `--author`: Filter by author
- `--branch`: Summarize specific branch
- `--format`: Output format (summary, changelog, release-notes)

### `validate` - Commit Message Validation

Check commit messages against formatting conventions.

```bash
# Validate last 10 commits
gitbrain validate

# Validate against Conventional Commits
gitbrain validate --conventional

# Suggest fixes for invalid messages
gitbrain validate --conventional --fix

# Validate specific commit range
gitbrain validate --range HEAD~5..HEAD
```

**Options:**
- `--range`: Validate specific commit range
- `--fix`: Suggest improved messages for invalid commits
- `--conventional`: Validate against Conventional Commits format

### `interactive-add` - AI-Assisted Staging

Get AI recommendations for staging changes.

```bash
# Launch interactive staging with AI analysis
gitbrain interactive-add
```

The tool will:
1. Analyze each file's changes
2. Provide AI recommendations
3. Ask whether to stage each change
4. Show diffs when requested

### `clean-branches` - Git Branch Cleanup

Clean up local and remote branches that have been merged into main/master.

```bash
# Clean only local merged branches
gitbrain clean-branches

# Clean both local and remote branches (with confirmation)
gitbrain clean-branches --remote

# Preview what would be deleted without actually deleting
gitbrain clean-branches --dry-run --remote

# Force deletion without confirmation prompts
gitbrain clean-branches --force --remote

# Generate shell aliases for easy reuse
gitbrain clean-branches --generate-alias
```

**Options:**
- `--remote, -r`: Also delete remote branches (requires confirmation)
- `--force, -f`: Skip confirmation prompts
- `--dry-run, -d`: Show what would be deleted without actually deleting
- `--generate-alias, -g`: Generate shell alias for quick reuse

**Safety Features:**
- Automatically switches to main/master branch and pulls latest changes
- Only deletes branches that are fully merged
- Requires confirmation for remote branch deletion (unless `--force`)
- Supports both `main` and `master` as the primary branch
- Safe dry-run mode to preview changes

### `install-hook` - Pre-commit Integration

Install Git hooks for automatic validation and message generation.

```bash
# Install pre-commit hook
gitbrain install-hook

# Remove pre-commit hook
gitbrain install-hook --uninstall
```

The hook will:
- Validate commit messages before commits
- Offer to generate messages if validation fails
- Support Conventional Commits validation

### `setup` & `status` - Configuration

Manage AI provider configuration.

```bash
# Interactive provider setup
gitbrain setup

# Setup specific provider
gitbrain setup ollama

# Check configuration status
gitbrain status
```

## 💡 Usage Examples

### Real-World Scenarios

#### 🔧 **Feature Development Workflow**

```bash
# 1. Start working on a new feature
vim src/auth.py
vim src/login.html
vim tests/test_auth.py

# 2. Check what you've changed
gitbrain explain
# Output: This adds user authentication functionality with login form and tests

# 3. Interactively stage changes with AI recommendations
gitbrain interactive-add
# AI will analyze each file and recommend whether to stage it

# 4. Generate a conventional commit
gitbrain commit --conventional
# Output: feat(auth): add user login functionality with form validation

# 5. Get branch name for next feature
gitbrain branch-suggest --create
# Creates and switches to: feat/password-reset
```

#### 🐛 **Bug Fix Workflow**

```bash
# 1. Fix a bug in existing code
vim src/api.py  # Fix timeout issue

# 2. Stage the fix
git add src/api.py

# 3. Generate commit with higher creativity for better description
gitbrain commit --temperature 1.2
# Output: Fix API timeout issue by increasing request timeout from 5s to 30s

# 4. Validate the commit message format
gitbrain validate --conventional --range HEAD~1..HEAD
# Ensures your commit follows standards
```

#### 📋 **Code Review Preparation**

```bash
# 1. Explain all changes for reviewers
gitbrain explain
# Get plain English explanation of your work

# 2. Summarize your feature branch
gitbrain summarize --branch feature/user-profiles
# Generate overview of all commits in the branch

# 3. Validate all commit messages in the branch
gitbrain validate --conventional --fix --range main..HEAD
# Check and get suggestions for improving commit messages
```

#### 🚀 **Release Preparation**

```bash
# 1. Generate changelog since last release
gitbrain summarize --format changelog --since "v1.2.0"

# 2. Create release notes
gitbrain summarize --format release-notes --since "v1.2.0"

# 3. Validate all commits since last release
gitbrain validate --conventional --range v1.2.0..HEAD

# 4. Install pre-commit hook for future quality
gitbrain install-hook
```

#### 🔍 **Understanding Legacy Code**

```bash
# 1. Understand changes in specific files
gitbrain explain --file src/legacy_module.py

# 2. Get summary of recent activity by specific author
gitbrain summarize --author "senior.dev@company.com" --since "1 month ago"

# 3. Analyze commit patterns
gitbrain validate --range HEAD~50..HEAD
```

### Advanced Usage Patterns

#### **Multi-file Analysis**
```bash
# Stage related files and get comprehensive explanation
git add src/models/ src/views/ src/templates/
gitbrain explain --staged
# AI explains how all the changes work together
```

#### **Branch Management**
```bash
# Get branch suggestions from any commit
gitbrain branch-suggest --from-commit abc123

# Create feature branches with AI-suggested names
git stash  # Save current work
gitbrain branch-suggest --create
git stash pop  # Resume work on new branch

# Clean up merged branches after successful PRs
gitbrain clean-branches --remote

# Preview what branches would be cleaned
gitbrain clean-branches --dry-run --remote
```

#### **Commit Message Refinement**
```bash
# Generate conventional commits with different creativity levels
gitbrain commit --conventional --temperature 0.2  # Conservative
gitbrain commit --conventional --temperature 1.5  # Creative

# Auto-commit for small changes
gitbrain commit --auto --conventional
```

#### **Team Collaboration**
```bash
# Summarize team activity
gitbrain summarize --since "1 week ago" --format summary

# Validate team's commit quality
gitbrain validate --conventional --range origin/main..HEAD
```

#### **Integration with Git Hooks**
```bash
# Install comprehensive pre-commit validation
gitbrain install-hook

# The hook automatically:
# - Validates commit message format
# - Offers AI-generated messages if validation fails
# - Ensures consistent commit quality across the team
```

### Command Combinations

#### **Complete Feature Development**
```bash
# The full AI-assisted development cycle
gitbrain interactive-add          # Smart staging
gitbrain commit --conventional    # Structured commit
gitbrain validate --conventional  # Quality check
gitbrain branch-suggest --create  # Next feature setup
```

#### **Code Review Package**
```bash
# Prepare comprehensive review materials
gitbrain explain > CHANGES.md
gitbrain summarize --format changelog >> CHANGES.md
gitbrain validate --conventional --fix
```

#### **Release Documentation**
```bash
# Generate complete release documentation
gitbrain summarize --format release-notes --since "v1.0.0" > RELEASE_NOTES.md
gitbrain summarize --format changelog --since "v1.0.0" > CHANGELOG.md
```

## 🤖 Supported AI Providers

| Provider | Models | API Key Required | Cost | Best For |
|----------|--------|------------------|------|----------|
| **OpenAI** | GPT-3.5-turbo, GPT-4, etc. | ✅ Yes | Pay per use | High quality, reliable |
| **Google Gemini** | Gemini Pro | ✅ Yes | Free tier available | Good balance of quality/cost |
| **Anthropic Claude** | Claude 3 Haiku, Sonnet, Opus | ✅ Yes | Pay per use | Detailed explanations |
| **Ollama** | Llama 3.2, Code Llama, etc. | ❌ No | Free (local) | Privacy, offline use |

## 📋 Example Workflows

### Daily Development Workflow

```bash
# 1. Work on your feature
vim src/feature.py

# 2. Get AI explanation of changes
gitbrain explain

# 3. Interactively stage changes with AI help
gitbrain interactive-add

# 4. Generate and commit with AI message
gitbrain commit --conventional

# 5. Get suggested branch name for next feature
gitbrain branch-suggest --create
```

### Release Preparation

```bash
# 1. Validate all commit messages
gitbrain validate --conventional --fix

# 2. Generate changelog for release
gitbrain summarize --format changelog --since "v1.0.0"

# 3. Create release notes
gitbrain summarize --format release-notes --since "v1.0.0"
```

### Code Review Preparation

```bash
# 1. Explain all changes for reviewers
gitbrain explain

# 2. Summarize the branch's purpose
gitbrain summarize --branch feature/new-auth

# 3. Validate commit message quality
gitbrain validate --conventional
```

### Post-Merge Branch Cleanup

```bash
# 1. After successful PR merge, clean up local branches
gitbrain clean-branches

# 2. Clean up both local and remote branches
gitbrain clean-branches --remote

# 3. Set up aliases for regular cleanup
gitbrain clean-branches --generate-alias

# 4. Regular maintenance with dry-run preview
gitbrain clean-branches --dry-run --remote
```

## ⚙️ Configuration

### Temperature Settings
Control AI creativity (0.0 = deterministic, 2.0 = very creative):
- **0.0-0.3**: Conservative, consistent messages
- **0.5-0.7**: Balanced (default)
- **1.0-1.5**: More creative and varied
- **1.5-2.0**: Highly creative, potentially unexpected

### Conventional Commits Support
Full support for [Conventional Commits](https://www.conventionalcommits.org/) format:
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test-related changes
- `chore`: Maintenance tasks

### Configuration File
Settings stored in `~/.gitbrain/config.json`:
```json
{
  "provider": "ollama",
  "api_keys": {},
  "settings": {
    "temperature": 0.7,
    "max_tokens": 150,
    "model": {
      "ollama": "llama3.2"
    }
  }
}
```

## 💡 Best Practices & Tips

### Workflow Integration

#### **Daily Development Routine**
1. **Morning Setup**: `gitbrain status` - Check your AI provider is ready
2. **Feature Work**: Use `gitbrain explain` to understand changes before committing
3. **Smart Staging**: `gitbrain interactive-add` for complex changes
4. **Quality Commits**: Always use `--conventional` flag for team projects
5. **Branch Management**: `gitbrain branch-suggest --create` for new features
6. **Post-Merge Cleanup**: `gitbrain clean-branches --remote` after successful PRs

#### **Team Best Practices**
```bash
# Setup pre-commit hooks for the entire team
gitbrain install-hook

# Establish commit standards
gitbrain validate --conventional --fix

# Regular commit quality audits
gitbrain validate --range origin/main..HEAD --conventional
```

#### **Effective Prompt Usage**
- **High Temperature (1.2-1.8)**: Creative branch names, detailed explanations
- **Low Temperature (0.2-0.5)**: Consistent commit messages, formal documentation
- **Medium Temperature (0.7-1.0)**: Balanced approach for daily use

#### **Command Chaining for Efficiency**
```bash
# Complete feature workflow in one go
gitbrain interactive-add && \
gitbrain commit --conventional && \
gitbrain branch-suggest --create

# Release preparation pipeline
gitbrain validate --conventional --fix && \
gitbrain summarize --format changelog > CHANGELOG.md && \
gitbrain summarize --format release-notes > RELEASE.md
```

### Performance Tips

#### **Optimize for Large Repositories**
```bash
# Focus on recent changes only
gitbrain summarize --since "1 week ago"

# Validate recent commits instead of entire history
gitbrain validate --range HEAD~20..HEAD

# Explain specific files instead of entire diff
gitbrain explain --file src/main.py
```

#### **Provider Selection by Use Case**
- **OpenAI GPT-4**: Complex code analysis, detailed explanations
- **Gemini Pro**: Balanced performance for daily commits
- **Claude**: Excellent for documentation and release notes
- **Ollama**: Fast local processing, privacy-sensitive projects

### Integration Examples

#### **VS Code Integration**
Add to your VS Code tasks.json:
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "AI Commit",
      "type": "shell",
      "command": "gitbrain commit --conventional",
      "group": "build"
    },
    {
      "label": "Explain Changes",
      "type": "shell", 
      "command": "gitbrain explain --staged",
      "group": "build"
    }
  ]
}
```

#### **Git Aliases**
```bash
# Add to ~/.gitconfig
[alias]
  ai-commit = !gitbrain commit --conventional
  ai-explain = !gitbrain explain
  ai-branch = !gitbrain branch-suggest --create
  ai-validate = !gitbrain validate --conventional
```

#### **Shell Aliases**
```bash
# Add to ~/.bashrc or ~/.zshrc
alias aic='gitbrain commit --conventional'
alias aie='gitbrain explain'
alias aib='gitbrain branch-suggest'
alias ais='gitbrain summarize'
alias aiv='gitbrain validate --conventional'
alias aicb='gitbrain clean-branches --remote'
```

## 🔧 Troubleshooting

### Common Issues

**Provider not configured:**
```bash
gitbrain setup
```

**Ollama connection issues:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if needed
ollama serve
```

**Git repository not found:**
```bash
# Ensure you're in a Git repository
git init
```

**No staged changes:**
```bash
# Stage your changes first
git add .
gitbrain commit
```

**Command not found after installation:**
```bash
# Make sure you're in the project directory and use full path
./bin/gitbrain status

# Or add to PATH
export PATH=$PATH:$(pwd)/bin
```

**Slow AI responses:**
```bash
# Switch to faster model
gitbrain setup  # Choose lighter model

# Use Ollama for fastest local processing
gitbrain setup ollama
```

### Debug Mode
For detailed error information, check the configuration and status:
```bash
gitbrain status
```

### Getting Help
```bash
# General help
gitbrain --help

# Command-specific help
gitbrain commit --help
gitbrain summarize --help
gitbrain validate --help
```

## 🧩 Advanced Usage

### Custom Prompts
The tool supports different prompt styles for different use cases:
- **Standard commits**: Clear, concise messages
- **Conventional commits**: Structured with type prefixes
- **Branch naming**: Short, semantic names
- **Explanations**: Detailed, educational descriptions

### Batch Operations
Process multiple files or commits efficiently:
```bash
# Validate entire project history
gitbrain validate --range HEAD~100..HEAD --conventional

# Explain changes across multiple files
gitbrain explain --staged
```

### Integration with Git Workflows
- **Pre-commit hooks**: Automatic validation
- **CI/CD integration**: Validate PR commit messages
- **Release automation**: Generate changelogs automatically

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.com) for local AI model support
- [OpenAI](https://openai.com) for GPT models
- [Anthropic](https://anthropic.com) for Claude models
- [Google](https://ai.google.dev) for Gemini models
- [Conventional Commits](https://conventionalcommits.org) for commit standards

---

**Made with ❤️ for developers who want smarter Git workflows**

