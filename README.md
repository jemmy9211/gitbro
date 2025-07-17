# 🧠 AI-Powered Git CLI Tool (gitbro v2.0)

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
| `commit` | Generate AI-powered commit messages | `gitbro commit --conventional` |
| `branch-suggest` | Suggest semantic branch names | `gitbro branch-suggest --create` |
| `explain` | Human-friendly diff explanations | `gitbro explain --staged` |
| `summarize` | Commit history summarization | `gitbro summarize --format changelog` |
| `validate` | Commit message format checking | `gitbro validate --conventional --fix` |
| `interactive-add` | AI-assisted staging | `gitbro interactive-add` |
| `clean-branches` | Clean merged local/remote branches | `gitbro clean-branches --remote` |
| `install-hook` | Pre-commit hook integration | `gitbro install-hook` |
| `setup` | Configure AI providers | `gitbro setup ollama` |
| `status` | Show configuration status | `gitbro status` |

## 📦 Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/gitbro.git
   cd gitbro
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
   gitbro setup
   ```
   Choose from the interactive menu or specify directly:
   ```bash
   gitbro setup openai    # For OpenAI
   gitbro setup gemini    # For Google Gemini
   gitbro setup claude    # For Anthropic Claude
   gitbro setup ollama    # For Ollama (local)
   ```

## 🎯 Quick Start Guide

### Getting Started with New Features

1. **Check your setup:**
   ```bash
   gitbro status
   ```

2. **Make some changes and stage them:**
   ```bash
   echo "console.log('Hello AI!');" > hello.js
   git add hello.js
   ```

3. **Generate an AI commit message:**
   ```bash
   gitbro commit
   # Output: Add hello.js with greeting message
   ```

4. **Get AI explanation of your changes:**
   ```bash
   gitbro explain --staged
   # Output: 📝 Change Explanation:
   # This change adds a new JavaScript file that prints a greeting message to the console...
   ```

5. **Get a semantic branch name suggestion:**
   ```bash
   gitbro branch-suggest
   # Output: Suggested branch name: feat/add-hello-script
   ```

## 🛠️ Command Reference

### `commit` - AI-Powered Commit Messages

Generate meaningful commit messages from staged changes.

```bash
# Basic usage
gitbro commit

# Use Conventional Commits format
gitbro commit --conventional

# Auto-commit without confirmation
gitbro commit --auto

# Adjust creativity level
gitbro commit --temperature 1.2
```

**Options:**
- `--temperature, -t`: AI creativity level (0.0-2.0)
- `--auto, -a`: Auto-commit with generated message
- `--conventional, -c`: Use Conventional Commits format

### `branch-suggest` - Semantic Branch Naming

Generate branch names based on code changes.

```bash
# Suggest branch name from staged changes
gitbro branch-suggest

# Auto-create the suggested branch
gitbro branch-suggest --create

# Generate name from specific commit
gitbro branch-suggest --from-commit abc123
```

**Options:**
- `--create, -c`: Auto-create the suggested branch
- `--from-commit`: Generate name from specific commit hash

### `explain` - Code Change Explanations

Get plain English explanations of your code changes.

```bash
# Explain working directory changes
gitbro explain

# Explain only staged changes
gitbro explain --staged

# Explain changes in specific file
gitbro explain --file src/main.py
```

**Options:**
- `--staged, -s`: Explain staged changes only
- `--file, -f`: Explain changes in specific file

### `summarize` - Commit History Analysis

Generate summaries, changelogs, and release notes from commit history.

```bash
# Basic summary of recent commits
gitbro summarize

# Generate a changelog
gitbro summarize --format changelog

# Create release notes
gitbro summarize --format release-notes

# Filter by time period
gitbro summarize --since "1 week ago"

# Filter by author
gitbro summarize --author "john@example.com"

# Summarize specific branch
gitbro summarize --branch feature/new-auth
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
gitbro validate

# Validate against Conventional Commits
gitbro validate --conventional

# Suggest fixes for invalid messages
gitbro validate --conventional --fix

# Validate specific commit range
gitbro validate --range HEAD~5..HEAD
```

**Options:**
- `--range`: Validate specific commit range
- `--fix`: Suggest improved messages for invalid commits
- `--conventional`: Validate against Conventional Commits format

### `interactive-add` - AI-Assisted Staging

Get AI recommendations for staging changes.

```bash
# Launch interactive staging with AI analysis
gitbro interactive-add
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
gitbro clean-branches

# Clean both local and remote branches (with confirmation)
gitbro clean-branches --remote

# Preview what would be deleted without actually deleting
gitbro clean-branches --dry-run --remote

# Force deletion without confirmation prompts
gitbro clean-branches --force --remote

# Generate shell aliases for easy reuse
gitbro clean-branches --generate-alias
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
gitbro install-hook

# Remove pre-commit hook
gitbro install-hook --uninstall
```

The hook will:
- Validate commit messages before commits
- Offer to generate messages if validation fails
- Support Conventional Commits validation

### `setup` & `status` - Configuration

Manage AI provider configuration.

```bash
# Interactive provider setup
gitbro setup

# Setup specific provider
gitbro setup ollama

# Check configuration status
gitbro status
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
gitbro explain
# Output: This adds user authentication functionality with login form and tests

# 3. Interactively stage changes with AI recommendations
gitbro interactive-add
# AI will analyze each file and recommend whether to stage it

# 4. Generate a conventional commit
gitbro commit --conventional
# Output: feat(auth): add user login functionality with form validation

# 5. Get branch name for next feature
gitbro branch-suggest --create
# Creates and switches to: feat/password-reset
```

#### 🐛 **Bug Fix Workflow**

```bash
# 1. Fix a bug in existing code
vim src/api.py  # Fix timeout issue

# 2. Stage the fix
git add src/api.py

# 3. Generate commit with higher creativity for better description
gitbro commit --temperature 1.2
# Output: Fix API timeout issue by increasing request timeout from 5s to 30s

# 4. Validate the commit message format
gitbro validate --conventional --range HEAD~1..HEAD
# Ensures your commit follows standards
```

#### 📋 **Code Review Preparation**

```bash
# 1. Explain all changes for reviewers
gitbro explain
# Get plain English explanation of your work

# 2. Summarize your feature branch
gitbro summarize --branch feature/user-profiles
# Generate overview of all commits in the branch

# 3. Validate all commit messages in the branch
gitbro validate --conventional --fix --range main..HEAD
# Check and get suggestions for improving commit messages
```

#### 🚀 **Release Preparation**

```bash
# 1. Generate changelog since last release
gitbro summarize --format changelog --since "v1.2.0"

# 2. Create release notes
gitbro summarize --format release-notes --since "v1.2.0"

# 3. Validate all commits since last release
gitbro validate --conventional --range v1.2.0..HEAD

# 4. Install pre-commit hook for future quality
gitbro install-hook
```

#### 🔍 **Understanding Legacy Code**

```bash
# 1. Understand changes in specific files
gitbro explain --file src/legacy_module.py

# 2. Get summary of recent activity by specific author
gitbro summarize --author "senior.dev@company.com" --since "1 month ago"

# 3. Analyze commit patterns
gitbro validate --range HEAD~50..HEAD
```

### Advanced Usage Patterns

#### **Multi-file Analysis**
```bash
# Stage related files and get comprehensive explanation
git add src/models/ src/views/ src/templates/
gitbro explain --staged
# AI explains how all the changes work together
```

#### **Branch Management**
```bash
# Get branch suggestions from any commit
gitbro branch-suggest --from-commit abc123

# Create feature branches with AI-suggested names
git stash  # Save current work
gitbro branch-suggest --create
git stash pop  # Resume work on new branch

# Clean up merged branches after successful PRs
gitbro clean-branches --remote

# Preview what branches would be cleaned
gitbro clean-branches --dry-run --remote
```

#### **Commit Message Refinement**
```bash
# Generate conventional commits with different creativity levels
gitbro commit --conventional --temperature 0.2  # Conservative
gitbro commit --conventional --temperature 1.5  # Creative

# Auto-commit for small changes
gitbro commit --auto --conventional
```

#### **Team Collaboration**
```bash
# Summarize team activity
gitbro summarize --since "1 week ago" --format summary

# Validate team's commit quality
gitbro validate --conventional --range origin/main..HEAD
```

#### **Integration with Git Hooks**
```bash
# Install comprehensive pre-commit validation
gitbro install-hook

# The hook automatically:
# - Validates commit message format
# - Offers AI-generated messages if validation fails
# - Ensures consistent commit quality across the team
```

### Command Combinations

#### **Complete Feature Development**
```bash
# The full AI-assisted development cycle
gitbro interactive-add          # Smart staging
gitbro commit --conventional    # Structured commit
gitbro validate --conventional  # Quality check
gitbro branch-suggest --create  # Next feature setup
```

#### **Code Review Package**
```bash
# Prepare comprehensive review materials
gitbro explain > CHANGES.md
gitbro summarize --format changelog >> CHANGES.md
gitbro validate --conventional --fix
```

#### **Release Documentation**
```bash
# Generate complete release documentation
gitbro summarize --format release-notes --since "v1.0.0" > RELEASE_NOTES.md
gitbro summarize --format changelog --since "v1.0.0" > CHANGELOG.md
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
gitbro explain

# 3. Interactively stage changes with AI help
gitbro interactive-add

# 4. Generate and commit with AI message
gitbro commit --conventional

# 5. Get suggested branch name for next feature
gitbro branch-suggest --create
```

### Release Preparation

```bash
# 1. Validate all commit messages
gitbro validate --conventional --fix

# 2. Generate changelog for release
gitbro summarize --format changelog --since "v1.0.0"

# 3. Create release notes
gitbro summarize --format release-notes --since "v1.0.0"
```

### Code Review Preparation

```bash
# 1. Explain all changes for reviewers
gitbro explain

# 2. Summarize the branch's purpose
gitbro summarize --branch feature/new-auth

# 3. Validate commit message quality
gitbro validate --conventional
```

### Post-Merge Branch Cleanup

```bash
# 1. After successful PR merge, clean up local branches
gitbro clean-branches

# 2. Clean up both local and remote branches
gitbro clean-branches --remote

# 3. Set up aliases for regular cleanup
gitbro clean-branches --generate-alias

# 4. Regular maintenance with dry-run preview
gitbro clean-branches --dry-run --remote
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
Settings stored in `~/.gitbro/config.json`:
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
1. **Morning Setup**: `gitbro status` - Check your AI provider is ready
2. **Feature Work**: Use `gitbro explain` to understand changes before committing
3. **Smart Staging**: `gitbro interactive-add` for complex changes
4. **Quality Commits**: Always use `--conventional` flag for team projects
5. **Branch Management**: `gitbro branch-suggest --create` for new features
6. **Post-Merge Cleanup**: `gitbro clean-branches --remote` after successful PRs

#### **Team Best Practices**
```bash
# Setup pre-commit hooks for the entire team
gitbro install-hook

# Establish commit standards
gitbro validate --conventional --fix

# Regular commit quality audits
gitbro validate --range origin/main..HEAD --conventional
```

#### **Effective Prompt Usage**
- **High Temperature (1.2-1.8)**: Creative branch names, detailed explanations
- **Low Temperature (0.2-0.5)**: Consistent commit messages, formal documentation
- **Medium Temperature (0.7-1.0)**: Balanced approach for daily use

#### **Command Chaining for Efficiency**
```bash
# Complete feature workflow in one go
gitbro interactive-add && \
gitbro commit --conventional && \
gitbro branch-suggest --create

# Release preparation pipeline
gitbro validate --conventional --fix && \
gitbro summarize --format changelog > CHANGELOG.md && \
gitbro summarize --format release-notes > RELEASE.md
```

### Performance Tips

#### **Optimize for Large Repositories**
```bash
# Focus on recent changes only
gitbro summarize --since "1 week ago"

# Validate recent commits instead of entire history
gitbro validate --range HEAD~20..HEAD

# Explain specific files instead of entire diff
gitbro explain --file src/main.py
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
      "command": "gitbro commit --conventional",
      "group": "build"
    },
    {
      "label": "Explain Changes",
      "type": "shell", 
      "command": "gitbro explain --staged",
      "group": "build"
    }
  ]
}
```

#### **Git Aliases**
```bash
# Add to ~/.gitconfig
[alias]
  ai-commit = !gitbro commit --conventional
  ai-explain = !gitbro explain
  ai-branch = !gitbro branch-suggest --create
  ai-validate = !gitbro validate --conventional
```

#### **Shell Aliases**
```bash
# Add to ~/.bashrc or ~/.zshrc
alias aic='gitbro commit --conventional'
alias aie='gitbro explain'
alias aib='gitbro branch-suggest'
alias ais='gitbro summarize'
alias aiv='gitbro validate --conventional'
alias aicb='gitbro clean-branches --remote'
```

## 🔧 Troubleshooting

### Common Issues

**Provider not configured:**
```bash
gitbro setup
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
gitbro commit
```

**Command not found after installation:**
```bash
# Make sure you're in the project directory and use full path
./bin/gitbro status

# Or add to PATH
export PATH=$PATH:$(pwd)/bin
```

**Slow AI responses:**
```bash
# Switch to faster model
gitbro setup  # Choose lighter model

# Use Ollama for fastest local processing
gitbro setup ollama
```

### Debug Mode
For detailed error information, check the configuration and status:
```bash
gitbro status
```

### Getting Help
```bash
# General help
gitbro --help

# Command-specific help
gitbro commit --help
gitbro summarize --help
gitbro validate --help
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
gitbro validate --range HEAD~100..HEAD --conventional

# Explain changes across multiple files
gitbro explain --staged
```

### Integration with Git Workflows
- **Pre-commit hooks**: Automatic validation
- **CI/CD integration**: Validate PR commit messages
- **Release automation**: Generate changelogs automatically


## Star
![GitHub stars](https://img.shields.io/github/stars/jemmy9211/gitbro)

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

