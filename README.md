# AI-Powered Git Commit Message Generator

A versatile command-line tool that generates meaningful Git commit messages from your staged changes using multiple AI providers. Choose from OpenAI GPT models, Google Gemini, Anthropic Claude, or local Ollama models.

## Features

- **Multiple AI Providers**: OpenAI, Google Gemini, Anthropic Claude, and Ollama
- **Secure API Key Management**: Encrypted local storage of API credentials
- **Interactive Setup**: Easy configuration wizard for each provider
- **Creativity Control**: Adjust temperature for more or less creative commit messages
- **Local & Cloud**: Use local models (Ollama) or cloud-based AI services
- **Cross-Platform**: Works on Linux, macOS, and Windows

## Supported AI Providers

| Provider | Models | API Key Required | Cost |
|----------|--------|------------------|------|
| **OpenAI** | GPT-3.5-turbo, GPT-4, etc. | ✅ Yes | Pay per use |
| **Google Gemini** | Gemini Pro | ✅ Yes | Free tier available |
| **Anthropic Claude** | Claude 3 Haiku, Sonnet, Opus | ✅ Yes | Pay per use |
| **Ollama** | Llama 3.2, Code Llama, etc. | ❌ No | Free (local) |

## Installation

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
   - Installs required dependencies (OpenAI, Anthropic, Google AI libraries)
   - Sets up the executable script

3. **Set Up an AI Provider:**
   ```bash
   ./bin/ollamacommit --setup
   ```
   Choose from the interactive menu or specify directly:
   ```bash
   ./bin/ollamacommit --setup openai    # For OpenAI
   ./bin/ollamacommit --setup gemini    # For Google Gemini
   ./bin/ollamacommit --setup claude    # For Anthropic Claude
   ./bin/ollamacommit --setup ollama    # For Ollama (local)
   ```

4. **(Optional) Add to PATH:**
   ```bash
   export PATH=$PATH:$(pwd)/bin
   ```
   Add this to your `~/.bashrc` or `~/.zshrc` for persistence.

## Getting API Keys

### OpenAI
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create an account and navigate to API Keys
3. Generate a new secret key
4. Copy the key for setup

### Google Gemini
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key for setup

### Anthropic Claude
1. Visit [Anthropic Console](https://console.anthropic.com/account/keys)
2. Create an account and verify your email
3. Generate a new API key
4. Copy the key for setup

### Ollama (Local)
1. Install Ollama from [ollama.com](https://ollama.com)
2. Start the service: `ollama serve`
3. Pull a model: `ollama pull llama3.2`
4. No API key required!

## Usage

### Basic Usage

1. **Stage your changes:**
   ```bash
   git add .
   ```

2. **Generate commit message:**
   ```bash
   ./bin/ollamacommit
   ```
   Or if added to PATH:
   ```bash
   ollamacommit
   ```

### Advanced Options

- **Check configuration status:**
  ```bash
  ./bin/ollamacommit --status
  ```

- **Switch providers:**
  ```bash
  ./bin/ollamacommit --provider openai
  ./bin/ollamacommit --provider gemini
  ./bin/ollamacommit --provider claude
  ./bin/ollamacommit --provider ollama
  ```

- **Reconfigure a provider:**
  ```bash
  ./bin/ollamacommit --setup openai
  ```

### Interactive Workflow

When you run the tool, you'll see:

```
Generated commit message:
Add user authentication middleware

Please choose an action:
1) Accept and commit
2) Regenerate with more creativity  
3) Cancel and exit
Enter your choice (1-3):
```

- **Option 1**: Commits with the generated message
- **Option 2**: Regenerates with higher temperature (more creative/varied)
- **Option 3**: Exits without committing

## Configuration

Configuration is stored in `~/.ollamacommit/config.json` with the following structure:

```json
{
  "provider": "openai",
  "api_keys": {
    "openai": "sk-...",
    "gemini": "AIza...",
    "claude": "sk-ant-..."
  },
  "settings": {
    "temperature": 0.7,
    "max_tokens": 150,
    "model": {
      "openai": "gpt-3.5-turbo",
      "gemini": "gemini-pro",
      "claude": "claude-3-haiku-20240307",
      "ollama": "llama3.2"
    }
  }
}
```

## Model Options

### OpenAI Models
- `gpt-3.5-turbo` (default, fast and cost-effective)
- `gpt-4` (more capable, higher cost)
- `gpt-4-turbo` (latest GPT-4 with better performance)

### Gemini Models
- `gemini-pro` (default, balanced performance)
- `gemini-pro-vision` (supports images)

### Claude Models
- `claude-3-haiku-20240307` (default, fast and economical)
- `claude-3-sonnet-20240229` (balanced performance)
- `claude-3-opus-20240229` (most capable)

### Ollama Models
- `llama3.2` (default, general purpose)
- `codellama` (optimized for code)
- `mistral` (efficient alternative)
- Any model available in Ollama

## Troubleshooting

### Common Issues

**"No provider configured"**
```bash
./bin/ollamacommit --setup
```

**API key errors**
- Verify your API key is correct
- Check your account has sufficient credits/quota
- Reconfigure: `./bin/ollamacommit --setup [provider]`

**Ollama connection failed**
```bash
# Ensure Ollama is running
ollama serve

# Verify model is available
ollama list

# Pull model if needed
ollama pull llama3.2
```

**No staged changes**
```bash
git add .  # Stage your changes first
```

### Error Messages

- **OpenAI API error**: Check API key and quota
- **Gemini API error**: Verify API key and request limits
- **Claude API error**: Confirm API key and usage limits
- **Ollama error**: Ensure service is running locally

## Uninstallation

```bash
./uninstall.sh
```

This script will:
- Remove the virtual environment
- Optionally remove downloaded models (Ollama)
- Optionally remove the AI provider applications

Configuration files in `~/.ollamacommit/` can be manually deleted.

## Security

- API keys are stored locally in `~/.ollamacommit/config.json`
- File permissions are set to user-only access (600)
- No data is transmitted except to your chosen AI provider
- For Ollama, everything runs locally with no external API calls

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### v2.0.0 - Multi-Provider Support
- Added support for OpenAI, Google Gemini, and Anthropic Claude
- Implemented secure API key management
- Added interactive provider setup
- Made Ollama optional instead of required
- Improved error handling and user experience

### v1.0.0 - Initial Release
- Basic Ollama integration
- Simple commit message generation

