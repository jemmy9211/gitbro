# 🧠 AI-Powered Git CLI Tool (ollamacommit v2.0)

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
| `commit` | Generate AI-powered commit messages | `ollamacommit commit --conventional` |
| `branch-suggest` | Suggest semantic branch names | `ollamacommit branch-suggest --create` |
| `explain` | Human-friendly diff explanations | `ollamacommit explain --staged` |
| `summarize` | Commit history summarization | `ollamacommit summarize --format changelog` |
| `validate` | Commit message format checking | `ollamacommit validate --conventional --fix` |
| `interactive-add` | AI-assisted staging | `ollamacommit interactive-add` |
| `install-hook` | Pre-commit hook integration | `ollamacommit install-hook` |
| `setup` | Configure AI providers | `ollamacommit setup ollama` |
| `status` | Show configuration status | `ollamacommit status` |

## 📦 Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/ollamacommit.git
   cd ollamacommit
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
   ollamacommit setup
   ```
   Choose from the interactive menu or specify directly:
   ```bash
   ollamacommit setup openai    # For OpenAI
   ollamacommit setup gemini    # For Google Gemini
   ollamacommit setup claude    # For Anthropic Claude
   ollamacommit setup ollama    # For Ollama (local)
   ```

## 🎯 Quick Start Guide

### Getting Started with New Features

1. **Check your setup:**
   ```bash
   ollamacommit status
   ```

2. **Make some changes and stage them:**
   ```bash
   echo "console.log('Hello AI!');" > hello.js
   git add hello.js
   ```

3. **Generate an AI commit message:**
   ```bash
   ollamacommit commit
   # Output: Add hello.js with greeting message
   ```

4. **Get AI explanation of your changes:**
   ```bash
   ollamacommit explain --staged
   # Output: 📝 Change Explanation:
   # This change adds a new JavaScript file that prints a greeting message to the console...
   ```

5. **Get a semantic branch name suggestion:**
   ```bash
   ollamacommit branch-suggest
   # Output: Suggested branch name: feat/add-hello-script
   ```

## 🛠️ Command Reference

### `commit` - AI-Powered Commit Messages

Generate meaningful commit messages from staged changes.

```bash
# Basic usage
ollamacommit commit

# Use Conventional Commits format
ollamacommit commit --conventional

# Auto-commit without confirmation
ollamacommit commit --auto

# Adjust creativity level
ollamacommit commit --temperature 1.2
```

**Options:**
- `--temperature, -t`: AI creativity level (0.0-2.0)
- `--auto, -a`: Auto-commit with generated message
- `--conventional, -c`: Use Conventional Commits format

### `branch-suggest` - Semantic Branch Naming

Generate branch names based on code changes.

```bash
# Suggest branch name from staged changes
ollamacommit branch-suggest

# Auto-create the suggested branch
ollamacommit branch-suggest --create

# Generate name from specific commit
ollamacommit branch-suggest --from-commit abc123
```

**Options:**
- `--create, -c`: Auto-create the suggested branch
- `--from-commit`: Generate name from specific commit hash

### `explain` - Code Change Explanations

Get plain English explanations of your code changes.

```bash
# Explain working directory changes
ollamacommit explain

# Explain only staged changes
ollamacommit explain --staged

# Explain changes in specific file
ollamacommit explain --file src/main.py
```

**Options:**
- `--staged, -s`: Explain staged changes only
- `--file, -f`: Explain changes in specific file

### `summarize` - Commit History Analysis

Generate summaries, changelogs, and release notes from commit history.

```bash
# Basic summary of recent commits
ollamacommit summarize

# Generate a changelog
ollamacommit summarize --format changelog

# Create release notes
ollamacommit summarize --format release-notes

# Filter by time period
ollamacommit summarize --since "1 week ago"

# Filter by author
ollamacommit summarize --author "john@example.com"

# Summarize specific branch
ollamacommit summarize --branch feature/new-auth
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
ollamacommit validate

# Validate against Conventional Commits
ollamacommit validate --conventional

# Suggest fixes for invalid messages
ollamacommit validate --conventional --fix

# Validate specific commit range
ollamacommit validate --range HEAD~5..HEAD
```

**Options:**
- `--range`: Validate specific commit range
- `--fix`: Suggest improved messages for invalid commits
- `--conventional`: Validate against Conventional Commits format

### `interactive-add` - AI-Assisted Staging

Get AI recommendations for staging changes.

```bash
# Launch interactive staging with AI analysis
ollamacommit interactive-add
```

The tool will:
1. Analyze each file's changes
2. Provide AI recommendations
3. Ask whether to stage each change
4. Show diffs when requested

### `install-hook` - Pre-commit Integration

Install Git hooks for automatic validation and message generation.

```bash
# Install pre-commit hook
ollamacommit install-hook

# Remove pre-commit hook
ollamacommit install-hook --uninstall
```

The hook will:
- Validate commit messages before commits
- Offer to generate messages if validation fails
- Support Conventional Commits validation

### `setup` & `status` - Configuration

Manage AI provider configuration.

```bash
# Interactive provider setup
ollamacommit setup

# Setup specific provider
ollamacommit setup ollama

# Check configuration status
ollamacommit status
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
ollamacommit explain
# Output: This adds user authentication functionality with login form and tests

# 3. Interactively stage changes with AI recommendations
ollamacommit interactive-add
# AI will analyze each file and recommend whether to stage it

# 4. Generate a conventional commit
ollamacommit commit --conventional
# Output: feat(auth): add user login functionality with form validation

# 5. Get branch name for next feature
ollamacommit branch-suggest --create
# Creates and switches to: feat/password-reset
```

#### 🐛 **Bug Fix Workflow**

```bash
# 1. Fix a bug in existing code
vim src/api.py  # Fix timeout issue

# 2. Stage the fix
git add src/api.py

# 3. Generate commit with higher creativity for better description
ollamacommit commit --temperature 1.2
# Output: Fix API timeout issue by increasing request timeout from 5s to 30s

# 4. Validate the commit message format
ollamacommit validate --conventional --range HEAD~1..HEAD
# Ensures your commit follows standards
```

#### 📋 **Code Review Preparation**

```bash
# 1. Explain all changes for reviewers
ollamacommit explain
# Get plain English explanation of your work

# 2. Summarize your feature branch
ollamacommit summarize --branch feature/user-profiles
# Generate overview of all commits in the branch

# 3. Validate all commit messages in the branch
ollamacommit validate --conventional --fix --range main..HEAD
# Check and get suggestions for improving commit messages
```

#### 🚀 **Release Preparation**

```bash
# 1. Generate changelog since last release
ollamacommit summarize --format changelog --since "v1.2.0"

# 2. Create release notes
ollamacommit summarize --format release-notes --since "v1.2.0"

# 3. Validate all commits since last release
ollamacommit validate --conventional --range v1.2.0..HEAD

# 4. Install pre-commit hook for future quality
ollamacommit install-hook
```

#### 🔍 **Understanding Legacy Code**

```bash
# 1. Understand changes in specific files
ollamacommit explain --file src/legacy_module.py

# 2. Get summary of recent activity by specific author
ollamacommit summarize --author "senior.dev@company.com" --since "1 month ago"

# 3. Analyze commit patterns
ollamacommit validate --range HEAD~50..HEAD
```

### Advanced Usage Patterns

#### **Multi-file Analysis**
```bash
# Stage related files and get comprehensive explanation
git add src/models/ src/views/ src/templates/
ollamacommit explain --staged
# AI explains how all the changes work together
```

#### **Branch Management**
```bash
# Get branch suggestions from any commit
ollamacommit branch-suggest --from-commit abc123

# Create feature branches with AI-suggested names
git stash  # Save current work
ollamacommit branch-suggest --create
git stash pop  # Resume work on new branch
```

#### **Commit Message Refinement**
```bash
# Generate conventional commits with different creativity levels
ollamacommit commit --conventional --temperature 0.2  # Conservative
ollamacommit commit --conventional --temperature 1.5  # Creative

# Auto-commit for small changes
ollamacommit commit --auto --conventional
```

#### **Team Collaboration**
```bash
# Summarize team activity
ollamacommit summarize --since "1 week ago" --format summary

# Validate team's commit quality
ollamacommit validate --conventional --range origin/main..HEAD
```

#### **Integration with Git Hooks**
```bash
# Install comprehensive pre-commit validation
ollamacommit install-hook

# The hook automatically:
# - Validates commit message format
# - Offers AI-generated messages if validation fails
# - Ensures consistent commit quality across the team
```

### Command Combinations

#### **Complete Feature Development**
```bash
# The full AI-assisted development cycle
ollamacommit interactive-add          # Smart staging
ollamacommit commit --conventional    # Structured commit
ollamacommit validate --conventional  # Quality check
ollamacommit branch-suggest --create  # Next feature setup
```

#### **Code Review Package**
```bash
# Prepare comprehensive review materials
ollamacommit explain > CHANGES.md
ollamacommit summarize --format changelog >> CHANGES.md
ollamacommit validate --conventional --fix
```

#### **Release Documentation**
```bash
# Generate complete release documentation
ollamacommit summarize --format release-notes --since "v1.0.0" > RELEASE_NOTES.md
ollamacommit summarize --format changelog --since "v1.0.0" > CHANGELOG.md
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
ollamacommit explain

# 3. Interactively stage changes with AI help
ollamacommit interactive-add

# 4. Generate and commit with AI message
ollamacommit commit --conventional

# 5. Get suggested branch name for next feature
ollamacommit branch-suggest --create
```

### Release Preparation

```bash
# 1. Validate all commit messages
ollamacommit validate --conventional --fix

# 2. Generate changelog for release
ollamacommit summarize --format changelog --since "v1.0.0"

# 3. Create release notes
ollamacommit summarize --format release-notes --since "v1.0.0"
```

### Code Review Preparation

```bash
# 1. Explain all changes for reviewers
ollamacommit explain

# 2. Summarize the branch's purpose
ollamacommit summarize --branch feature/new-auth

# 3. Validate commit message quality
ollamacommit validate --conventional
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
Settings stored in `~/.ollamacommit/config.json`:
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
1. **Morning Setup**: `ollamacommit status` - Check your AI provider is ready
2. **Feature Work**: Use `ollamacommit explain` to understand changes before committing
3. **Smart Staging**: `ollamacommit interactive-add` for complex changes
4. **Quality Commits**: Always use `--conventional` flag for team projects
5. **Branch Management**: `ollamacommit branch-suggest --create` for new features

#### **Team Best Practices**
```bash
# Setup pre-commit hooks for the entire team
ollamacommit install-hook

# Establish commit standards
ollamacommit validate --conventional --fix

# Regular commit quality audits
ollamacommit validate --range origin/main..HEAD --conventional
```

#### **Effective Prompt Usage**
- **High Temperature (1.2-1.8)**: Creative branch names, detailed explanations
- **Low Temperature (0.2-0.5)**: Consistent commit messages, formal documentation
- **Medium Temperature (0.7-1.0)**: Balanced approach for daily use

#### **Command Chaining for Efficiency**
```bash
# Complete feature workflow in one go
ollamacommit interactive-add && \
ollamacommit commit --conventional && \
ollamacommit branch-suggest --create

# Release preparation pipeline
ollamacommit validate --conventional --fix && \
ollamacommit summarize --format changelog > CHANGELOG.md && \
ollamacommit summarize --format release-notes > RELEASE.md
```

### Performance Tips

#### **Optimize for Large Repositories**
```bash
# Focus on recent changes only
ollamacommit summarize --since "1 week ago"

# Validate recent commits instead of entire history
ollamacommit validate --range HEAD~20..HEAD

# Explain specific files instead of entire diff
ollamacommit explain --file src/main.py
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
      "command": "ollamacommit commit --conventional",
      "group": "build"
    },
    {
      "label": "Explain Changes",
      "type": "shell", 
      "command": "ollamacommit explain --staged",
      "group": "build"
    }
  ]
}
```

#### **Git Aliases**
```bash
# Add to ~/.gitconfig
[alias]
  ai-commit = !ollamacommit commit --conventional
  ai-explain = !ollamacommit explain
  ai-branch = !ollamacommit branch-suggest --create
  ai-validate = !ollamacommit validate --conventional
```

#### **Shell Aliases**
```bash
# Add to ~/.bashrc or ~/.zshrc
alias aic='ollamacommit commit --conventional'
alias aie='ollamacommit explain'
alias aib='ollamacommit branch-suggest'
alias ais='ollamacommit summarize'
alias aiv='ollamacommit validate --conventional'
```

## 🔧 Troubleshooting

### Common Issues

**Provider not configured:**
```bash
ollamacommit setup
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
ollamacommit commit
```

**Command not found after installation:**
```bash
# Make sure you're in the project directory and use full path
./bin/ollamacommit status

# Or add to PATH
export PATH=$PATH:$(pwd)/bin
```

**Slow AI responses:**
```bash
# Switch to faster model
ollamacommit setup  # Choose lighter model

# Use Ollama for fastest local processing
ollamacommit setup ollama
```

### Debug Mode
For detailed error information, check the configuration and status:
```bash
ollamacommit status
```

### Getting Help
```bash
# General help
ollamacommit --help

# Command-specific help
ollamacommit commit --help
ollamacommit summarize --help
ollamacommit validate --help
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
ollamacommit validate --range HEAD~100..HEAD --conventional

# Explain changes across multiple files
ollamacommit explain --staged
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

